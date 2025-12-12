"""GitHub API client with authentication and rate limiting."""

import asyncio
import base64
import json
import os
import subprocess
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.parse import quote

import httpx

from .exceptions import (
    AuthenticationError,
    NetworkError,
    RateLimitError,
    APIError,
    RepositoryNotFoundError,
    OrganizationNotFoundError,
    TeamNotFoundError,
    wrap_exception,
    get_error_context
)
from .logging_config import get_logger, log_exception, log_rate_limit
from .smart_rate_limiter import handle_smart_rate_limiting, handle_rate_limit_exceeded
from .models import APIResponse, FileContent, FileInfo, Repository
from .batch_models import BatchRequest, BatchResult, BatchConfig
from .github_app_auth import create_github_app_auth, GitHubAppAuth

logger = get_logger(__name__)


def _format_reset_time(reset_time: int) -> str:
    """Format rate limit reset time safely, handling invalid timestamps."""
    if reset_time and reset_time > 0:
        return f"Resets at {datetime.fromtimestamp(reset_time)}"
    return "reset time unknown"


class GitHubClient:
    """Client for interacting with the GitHub API with rate limiting and ETag support."""

    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None, config: Optional[BatchConfig] = None, 
                 github_app_config: Optional[str] = None, org: Optional[str] = None) -> None:
        """Initialize the GitHub client with authentication token.
        
        Args:
            token: GitHub personal access token. If None, will attempt auto-discovery.
            config: Batch processing configuration
            github_app_config: Path to GitHub App configuration file
            org: Organization name (required for GitHub App auth)
        """
        # Authentication priority:
        # 1. Explicit token parameter
        # 2. GitHub App authentication (if config available and org provided)
        # 3. Token discovery (GITHUB_TOKEN env var or gh auth token)
        
        self.github_app_auth: Optional[GitHubAppAuth] = None
        self.org = org
        
        if token:
            # Explicit token provided - use it directly
            self.token = token
            logger.debug("Using explicitly provided token")
        elif github_app_config or (org and create_github_app_auth()):
            # Try GitHub App authentication
            try:
                self.github_app_auth = create_github_app_auth(github_app_config)
                if self.github_app_auth and org:
                    self.token = self.github_app_auth.get_token(org)
                    logger.info(f"✅ Using GitHub App authentication for organization '{org}'")
                else:
                    logger.debug("GitHub App auth not available, falling back to token discovery")
                    self.token = self._discover_token()
            except Exception as e:
                logger.warning(f"GitHub App authentication failed, falling back to token: {e}")
                self.token = self._discover_token()
        else:
            # Fall back to token discovery
            self.token = self._discover_token()
        
        self.config = config or BatchConfig()
        self.client = httpx.Client(
            base_url=self.BASE_URL,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "github-ioc-scanner/0.1.0",
            },
            timeout=30.0,
        )
        # Async client for batch operations
        self._async_client: Optional[httpx.AsyncClient] = None
        self._async_client_lock = asyncio.Lock()
        
        # Code Search API rate limit tracking
        self._code_search_rate_limited = False
        self._code_search_reset_time = 0
        
    def _discover_token(self) -> str:
        """Discover GitHub token from environment or gh CLI."""
        # Try GITHUB_TOKEN environment variable first
        token = os.getenv("GITHUB_TOKEN")
        if token:
            logger.debug("Using GITHUB_TOKEN environment variable")
            return token
            
        # Try gh auth token command
        try:
            result = subprocess.run(
                ["gh", "auth", "token"],
                capture_output=True,
                text=True,
                check=True,
                timeout=10,
            )
            token = result.stdout.strip()
            if token:
                logger.debug("Using token from 'gh auth token' command")
                return token
        except subprocess.CalledProcessError as e:
            logger.debug(f"'gh auth token' command failed with exit code {e.returncode}")
        except subprocess.TimeoutExpired:
            logger.debug("'gh auth token' command timed out")
        except FileNotFoundError:
            logger.debug("'gh' command not found in PATH")
        except Exception as e:
            logger.debug(f"Unexpected error running 'gh auth token': {e}")
            
        raise AuthenticationError(
            "No GitHub token found. Please set GITHUB_TOKEN environment variable or run 'gh auth login'"
        )
    
    def _refresh_token_if_needed(self) -> bool:
        """Refresh GitHub App token if needed and available.
        
        Returns:
            True if token was refreshed, False otherwise
        """
        if self.github_app_auth and self.org:
            try:
                new_token = self.github_app_auth.get_token(self.org)
                if new_token != self.token:
                    old_token_prefix = self.token[:10] if self.token else "None"
                    self.token = new_token
                    # Update client headers
                    self.client.headers["Authorization"] = f"Bearer {self.token}"
                    logger.info(f"🔄 Refreshed GitHub App token: {old_token_prefix}... → {self.token[:10]}...")
                    return True
                else:
                    logger.debug("GitHub App token is still valid")
                    return False
            except Exception as e:
                logger.warning(f"Failed to refresh GitHub App token: {e}")
                return False
        return False
    
    def _handle_network_error_with_retry(self, error_type: str, method: str, url: str, headers: Dict[str, Any], 
                                        params: Optional[Dict[str, Any]] = None, etag: Optional[str] = None, 
                                        original_error: Exception = None, max_retries: int = 3, **kwargs: Any) -> APIResponse:
        """Handle network errors with exponential backoff retry.
        
        Args:
            error_type: Type of network error (for logging)
            method: HTTP method
            url: Request URL
            headers: Request headers
            params: Request parameters
            etag: ETag for conditional requests
            original_error: The original network error
            max_retries: Maximum number of retry attempts
            **kwargs: Additional request arguments
            
        Returns:
            APIResponse from successful retry
            
        Raises:
            NetworkError: If all retries fail
        """
        import time
        import random
        
        for attempt in range(max_retries):
            # Calculate exponential backoff with jitter
            base_delay = 2 ** attempt  # 1s, 2s, 4s, 8s...
            jitter = random.uniform(0.1, 0.5)  # Add randomness to avoid thundering herd
            delay = base_delay + jitter
            
            logger.warning(f"🔄 {error_type.title()} for {url} - attempt {attempt + 1}/{max_retries}, retrying in {delay:.1f}s...")
            time.sleep(delay)
            
            try:
                # Retry the request
                response = self.client.request(method, url, headers=headers, params=params, **kwargs)
                
                # Process the retry response
                remaining = int(response.headers.get("X-RateLimit-Remaining", 0))
                reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
                
                # Handle rate limiting
                if response.status_code == 403:
                    error_message = response.text.lower()
                    if "rate limit exceeded" in error_message or "api rate limit exceeded" in error_message:
                        reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
                        raise RateLimitError(
                            f"GitHub API rate limit exceeded. {_format_reset_time(reset_time)}",
                            reset_time=reset_time
                        )
                
                # Handle 304 Not Modified
                if response.status_code == 304:
                    return APIResponse(
                        data=None,
                        etag=etag,
                        not_modified=True,
                        rate_limit_remaining=remaining,
                        rate_limit_reset=reset_time,
                    )
                
                response.raise_for_status()
                
                try:
                    data = response.json() if response.content else None
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse JSON response from {url}: {e}")
                    data = None
                
                logger.info(f"✅ Request successful after {error_type} retry (attempt {attempt + 1})")
                return APIResponse(
                    data=data,
                    etag=response.headers.get("ETag"),
                    not_modified=False,
                    rate_limit_remaining=remaining,
                    rate_limit_reset=reset_time,
                )
                
            except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.RequestError) as retry_error:
                if attempt == max_retries - 1:  # Last attempt
                    logger.error(f"🚨 All {max_retries} retry attempts failed for {url}")
                    raise NetworkError(f"{error_type.title()} from GitHub API: {url} (after {max_retries} retries)", cause=original_error)
                else:
                    logger.warning(f"   Retry attempt {attempt + 1} failed: {retry_error}")
                    continue
            except Exception as retry_error:
                # Other errors (like HTTP errors) should not be retried
                logger.warning(f"   Retry attempt {attempt + 1} failed with non-network error: {retry_error}")
                raise
        
        # This should not be reached, but just in case
        raise NetworkError(f"{error_type.title()} from GitHub API: {url} (after {max_retries} retries)", cause=original_error)
    
    def _make_request(
        self, 
        method: str, 
        url: str, 
        etag: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> APIResponse:
        """Make a request to the GitHub API with rate limiting and ETag support."""
        headers = kwargs.pop("headers", {})
        
        # Add ETag for conditional requests
        if etag:
            headers["If-None-Match"] = etag
            
        try:
            response = self.client.request(method, url, headers=headers, params=params, **kwargs)
            
            # Extract rate limit information
            remaining = int(response.headers.get("X-RateLimit-Remaining", 0))
            reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
            
            # Handle rate limiting (403 with rate limit message)
            if response.status_code == 403:
                error_message = response.text.lower()
                if "rate limit exceeded" in error_message or "api rate limit exceeded" in error_message:
                    reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
                    raise RateLimitError(
                        f"GitHub API rate limit exceeded. {_format_reset_time(reset_time)}",
                        reset_time=reset_time
                    )
                elif "forbidden" in error_message:
                    raise AuthenticationError("Access forbidden. Check token permissions for this resource.")
                else:
                    raise APIError(f"Forbidden: {response.text}", status_code=403)
            
            # Log rate limit information only for successful responses (not errors)
            # This prevents false "rate limit exhausted" warnings on auth errors
            if response.status_code < 400:
                log_rate_limit(logger, remaining, reset_time)
                # Proactive rate limit handling - slow down when approaching limits
                handle_smart_rate_limiting(remaining, reset_time)
            
            # Handle 304 Not Modified
            if response.status_code == 304:
                logger.debug(f"Resource not modified: {url}")
                return APIResponse(
                    data=None,
                    etag=etag,
                    not_modified=True,
                    rate_limit_remaining=remaining,
                    rate_limit_reset=reset_time,
                )
            
            # Handle other HTTP errors
            response.raise_for_status()
            
            # Parse response data
            try:
                data = response.json() if response.content else None
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse JSON response from {url}: {e}")
                data = None
            
            return APIResponse(
                data=data,
                etag=response.headers.get("ETag"),
                not_modified=False,
                rate_limit_remaining=remaining,
                rate_limit_reset=reset_time,
            )
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                # Try token refresh and retry if GitHub App is available
                if self.github_app_auth and self.org:
                    logger.warning("🔄 Received 401 Unauthorized - attempting GitHub App token refresh...")
                    try:
                        # Refresh token
                        refreshed = self._refresh_token_if_needed()
                        if refreshed:
                            # Update headers with new token
                            headers["Authorization"] = f"Bearer {self.token}"
                            
                            # Retry the request
                            retry_response = self.client.request(method, url, headers=headers, params=params, **kwargs)
                            
                            # Process the retry response
                            remaining = int(retry_response.headers.get("X-RateLimit-Remaining", 0))
                            reset_time = int(retry_response.headers.get("X-RateLimit-Reset", 0))
                            
                            if retry_response.status_code == 304:
                                return APIResponse(
                                    data=None,
                                    etag=etag,
                                    not_modified=True,
                                    rate_limit_remaining=remaining,
                                    rate_limit_reset=reset_time,
                                )
                            
                            retry_response.raise_for_status()
                            
                            try:
                                retry_data = retry_response.json() if retry_response.content else None
                            except json.JSONDecodeError as e:
                                logger.warning(f"Failed to parse JSON response from {url}: {e}")
                                retry_data = None
                            
                            logger.info("✅ Request successful after GitHub App token refresh")
                            return APIResponse(
                                data=retry_data,
                                etag=retry_response.headers.get("ETag"),
                                not_modified=False,
                                rate_limit_remaining=remaining,
                                rate_limit_reset=reset_time,
                            )
                    except Exception as retry_error:
                        logger.warning(f"Token refresh retry failed: {retry_error}")
                        pass  # Fall through to original error
                else:
                    logger.debug("Token refresh not attempted (no new token available)")
                
                # Check if this might be a repository access issue
                if "/repos/" in url:
                    repo_path = url.split("/repos/")[1].split("/")[0]
                    logger.warning(f"Access denied to repository: {repo_path} - may be private or restricted")
                
                raise AuthenticationError("Invalid GitHub token or insufficient permissions")
            elif e.response.status_code == 404:
                logger.debug(f"Resource not found: {url}")
                return APIResponse(data=None)
            elif e.response.status_code == 409:
                # Handle empty repositories gracefully
                error_text = e.response.text.lower()
                if "empty" in error_text or "repository is empty" in error_text:
                    logger.debug(f"Empty repository detected: {url}")
                    return APIResponse(data=None)
                else:
                    raise APIError(f"Conflict: {e.response.text}", status_code=409)
            elif e.response.status_code == 422:
                raise APIError(f"Unprocessable entity: {e.response.text}", status_code=422)
            else:
                raise APIError(f"HTTP {e.response.status_code}: {e.response.text}", status_code=e.response.status_code)
        except httpx.ConnectTimeout as e:
            # Retry connection timeouts with exponential backoff
            return self._handle_network_error_with_retry("connection timeout", method, url, headers, params, etag, e, **kwargs)
        except httpx.ReadTimeout as e:
            # Retry read timeouts with exponential backoff
            return self._handle_network_error_with_retry("read timeout", method, url, headers, params, etag, e, **kwargs)
        except httpx.RequestError as e:
            # Retry other network errors with exponential backoff
            return self._handle_network_error_with_retry("network error", method, url, headers, params, etag, e, **kwargs)
        except (RateLimitError, AuthenticationError, APIError, NetworkError):
            # These are expected exceptions that should be re-raised as-is
            raise
        except Exception as e:
            log_exception(logger, f"Unexpected error making request to {url}", e)
            raise wrap_exception(e, f"Unexpected error making request to {url}")
    
    def _handle_rate_limit(self, reset_time: int) -> None:
        """Handle rate limiting with exponential backoff."""
        handle_rate_limit_exceeded(reset_time)

    def get_organization_repos(
        self, org: str, include_archived: bool = False, etag: Optional[str] = None
    ) -> APIResponse:
        """Get all repositories for an organization.
        
        Args:
            org: Organization name
            include_archived: Whether to include archived repositories
            etag: ETag for conditional requests
            
        Returns:
            APIResponse containing list of Repository objects
            
        Raises:
            OrganizationNotFoundError: If the organization doesn't exist or is inaccessible
            AuthenticationError: If authentication fails
            NetworkError: If network operations fail
        """
        try:
            url = f"/orgs/{quote(org)}/repos"
            params = {
                "type": "all",
                "per_page": 100,
                "sort": "updated",
            }
            
            all_repos = []
            page = 1
            
            logger.info(f"Using REST API for repository discovery (fallback mode)")
            
            while True:
                params["page"] = page
                logger.info(f"Fetching repositories page {page} for organization {org}...")
                
                # Show progress on console (overwrite same line)
                print(f"\r   Loading page {page}... ({len(all_repos)} repositories found)", end='', flush=True)
                
                response = self._make_request("GET", url, etag=etag if page == 1 else None, params=params)
                
                if response.not_modified and page == 1:
                    print()  # New line after progress
                    return response
                    
                if not response.data:
                    # Empty response could mean organization not found or no repos
                    if page == 1:
                        print()  # New line after progress
                        raise OrganizationNotFoundError(org)
                    break
                    
                repos_data = response.data
                if not repos_data:
                    break
                    
                try:
                    page_repos = 0
                    for repo_data in repos_data:
                        if not include_archived and repo_data.get("archived", False):
                            continue
                            
                        repo = Repository(
                            name=repo_data["name"],
                            full_name=repo_data["full_name"],
                            archived=repo_data.get("archived", False),
                            default_branch=repo_data.get("default_branch", "main"),
                            updated_at=datetime.fromisoformat(repo_data["updated_at"].replace("Z", "+00:00")),
                        )
                        all_repos.append(repo)
                        page_repos += 1
                        
                    logger.info(f"Page {page}: Found {page_repos} repositories (total: {len(all_repos)})")
                    
                except (KeyError, ValueError, TypeError) as e:
                    logger.warning(f"Malformed repository data in organization {org}: {e}")
                    continue
                
                # Check if there are more pages
                if len(repos_data) < params["per_page"]:
                    break
                    
                page += 1
            
            # Clear progress line and show final count
            print(f"\r   ✓ Loaded {len(all_repos)} repositories from {page} page(s)          ")
            logger.info(f"Retrieved {len(all_repos)} repositories for organization {org}")
            
            return APIResponse(
                data=all_repos,
                etag=response.etag,
                not_modified=False,
                rate_limit_remaining=response.rate_limit_remaining,
                rate_limit_reset=response.rate_limit_reset,
            )
            
        except RateLimitError as e:
            # Handle rate limit gracefully - wait and retry once
            logger.warning(f"🚨 Rate limit hit while fetching repositories for {org}: {e}")
            self._handle_rate_limit(e.reset_time if hasattr(e, 'reset_time') else int(time.time()) + 3600)
            
            # Retry once after waiting
            try:
                logger.info(f"🔄 Retrying repository fetch for {org} after rate limit wait...")
                response = self._make_request("GET", url, etag=etag, params={"type": "all", "per_page": 100, "sort": "updated", "page": 1})
                
                if response.data:
                    # Process first page only for retry
                    repos_data = response.data
                    all_repos = []
                    
                    for repo_data in repos_data:
                        if not include_archived and repo_data.get("archived", False):
                            continue
                            
                        repo = Repository(
                            name=repo_data["name"],
                            full_name=repo_data["full_name"],
                            archived=repo_data.get("archived", False),
                            default_branch=repo_data.get("default_branch", "main"),
                            updated_at=datetime.fromisoformat(repo_data["updated_at"].replace("Z", "+00:00")),
                        )
                        all_repos.append(repo)
                    
                    logger.info(f"✅ Successfully retrieved {len(all_repos)} repositories for {org} after retry")
                    
                    return APIResponse(
                        data=all_repos,
                        etag=response.etag,
                        not_modified=False,
                        rate_limit_remaining=response.rate_limit_remaining,
                        rate_limit_reset=response.rate_limit_reset,
                    )
                else:
                    logger.info(f"No repositories found for {org} after retry")
                    return APIResponse(data=[])
                    
            except Exception as retry_e:
                logger.error(f"❌ Retry failed for {org}: {retry_e}")
                return APIResponse(data=[])  # Return empty instead of crashing
                
        except (OrganizationNotFoundError, AuthenticationError, NetworkError):
            raise
        except Exception as e:
            log_exception(logger, f"Failed to get repositories for organization {org}", e)
            return APIResponse(data=[])  # Return empty instead of crashing

    def get_organization_repos_graphql(
        self, org: str, include_archived: bool = False, 
        cached_repos: Optional[List[Repository]] = None,
        cache_cutoff: Optional[datetime] = None
    ) -> APIResponse:
        """Get all repositories for an organization using GraphQL (faster for large orgs).
        
        GraphQL allows fetching 100 repos per request with cursor-based pagination,
        which is more efficient than REST API pagination.
        
        Supports incremental fetching: if cached_repos and cache_cutoff are provided,
        only fetches repos updated after the cutoff and merges with cached repos.
        
        Args:
            org: Organization name
            include_archived: Whether to include archived repositories
            cached_repos: Previously cached repositories (for incremental update)
            cache_cutoff: Only fetch repos updated after this timestamp
            
        Returns:
            APIResponse containing list of Repository objects
        """
        try:
            # Sort by PUSHED_AT (most recently pushed first) for incremental fetching
            query = """
            query($org: String!, $cursor: String) {
                organization(login: $org) {
                    repositories(first: 100, after: $cursor, orderBy: {field: PUSHED_AT, direction: DESC}) {
                        pageInfo {
                            hasNextPage
                            endCursor
                        }
                        nodes {
                            name
                            nameWithOwner
                            isArchived
                            defaultBranchRef {
                                name
                            }
                            updatedAt
                            pushedAt
                        }
                    }
                }
            }
            """
            
            new_repos = []
            cursor = None
            page = 1
            stop_fetching = False
            incremental_mode = cached_repos is not None and cache_cutoff is not None
            
            if incremental_mode:
                logger.info(f"Using incremental GraphQL fetch (cutoff: {cache_cutoff})")
                print(f"   🔄 Checking for new/updated repositories...", end='', flush=True)
            else:
                logger.info(f"Using GraphQL API for repository discovery (faster for large orgs)")
            
            while True:
                if not incremental_mode:
                    print(f"\r   Loading page {page}... ({len(new_repos)} repositories found)", end='', flush=True)
                
                variables = {"org": org, "cursor": cursor}
                
                response = self.client.post(
                    f"{self.BASE_URL}/graphql",
                    json={"query": query, "variables": variables},
                    timeout=30.0
                )
                
                if response.status_code == 401:
                    print()
                    raise AuthenticationError("Invalid or expired GitHub token")
                elif response.status_code == 403:
                    # Check for rate limiting
                    if 'rate limit' in response.text.lower():
                        print()
                        raise RateLimitError("GraphQL rate limit exceeded")
                    raise AuthenticationError(f"Access denied to organization {org}")
                elif response.status_code != 200:
                    print()
                    raise APIError(f"GraphQL request failed: {response.status_code}")
                
                data = response.json()
                
                if 'errors' in data:
                    print()
                    error_msg = data['errors'][0].get('message', 'Unknown GraphQL error')
                    if 'Could not resolve to an Organization' in error_msg:
                        raise OrganizationNotFoundError(org)
                    raise APIError(f"GraphQL error: {error_msg}")
                
                org_data = data.get('data', {}).get('organization', {})
                repos_data = org_data.get('repositories', {})
                nodes = repos_data.get('nodes', [])
                page_info = repos_data.get('pageInfo', {})
                
                for repo_data in nodes:
                    if not include_archived and repo_data.get('isArchived', False):
                        continue
                    
                    # Check if we've reached repos older than our cache cutoff
                    if incremental_mode and repo_data.get('pushedAt'):
                        pushed_at = datetime.fromisoformat(repo_data['pushedAt'].replace('Z', '+00:00'))
                        if pushed_at < cache_cutoff:
                            # This repo and all following are older than cache - stop fetching
                            stop_fetching = True
                            break
                    
                    default_branch = 'main'
                    if repo_data.get('defaultBranchRef'):
                        default_branch = repo_data['defaultBranchRef'].get('name', 'main')
                    
                    repo = Repository(
                        name=repo_data['name'],
                        full_name=repo_data['nameWithOwner'],
                        archived=repo_data.get('isArchived', False),
                        default_branch=default_branch,
                        updated_at=datetime.fromisoformat(repo_data['updatedAt'].replace('Z', '+00:00')),
                    )
                    new_repos.append(repo)
                
                if stop_fetching or not page_info.get('hasNextPage', False):
                    break
                
                cursor = page_info.get('endCursor')
                page += 1
            
            # Merge with cached repos if in incremental mode
            if incremental_mode:
                if new_repos:
                    # Create a set of new repo names for fast lookup
                    new_repo_names = {repo.full_name for repo in new_repos}
                    
                    # Add cached repos that weren't updated
                    for cached_repo in cached_repos:
                        if cached_repo.full_name not in new_repo_names:
                            new_repos.append(cached_repo)
                    
                    print(f"\r   ✅ Found {len(new_repos) - len(cached_repos) + len([r for r in cached_repos if r.full_name in new_repo_names])} new/updated repos, {len(new_repos)} total    ")
                    logger.info(f"Incremental fetch: {len(new_repos)} total repos ({page} pages fetched)")
                else:
                    # No new repos, use cached repos
                    new_repos = list(cached_repos)
                    print(f"\r   ✅ No new repositories (using {len(new_repos)} cached)              ")
                    logger.info(f"No new repos since {cache_cutoff}, using {len(new_repos)} cached repos")
            else:
                print(f"\r   ✓ Loaded {len(new_repos)} repositories from {page} page(s) (GraphQL)    ")
                logger.info(f"Retrieved {len(new_repos)} repositories for organization {org} via GraphQL")
            
            return APIResponse(
                data=new_repos,
                etag=None,
                not_modified=False,
                rate_limit_remaining=None,
                rate_limit_reset=None,
            )
            
        except (OrganizationNotFoundError, AuthenticationError, RateLimitError):
            raise
        except Exception as e:
            logger.warning(f"GraphQL failed, falling back to REST: {e}")
            return self.get_organization_repos(org, include_archived)

    def get_organization_teams(self, org: str) -> List[Dict[str, Any]]:
        """Get all teams in an organization.
        
        Args:
            org: Organization name
            
        Returns:
            List of team dictionaries containing team information
            
        Raises:
            OrganizationNotFoundError: If the organization doesn't exist or is inaccessible
            AuthenticationError: If authentication fails
            NetworkError: If network operations fail
        """
        try:
            url = f"/orgs/{quote(org)}/teams"
            params = {
                "per_page": 100,
            }
            
            all_teams = []
            page = 1
            
            while True:
                params["page"] = page
                logger.info(f"Fetching teams page {page} for organization {org}...")
                
                # Show progress on console
                print(f"\r   Loading page {page}... ({len(all_teams)} teams found)", end='', flush=True)
                
                response = self._make_request("GET", url, params=params)
                
                if not response.data:
                    if page == 1:
                        print()  # New line after progress
                        logger.info(f"No teams found for organization {org}")
                        break
                    break
                    
                teams_data = response.data
                if not teams_data:
                    break
                    
                try:
                    for team_data in teams_data:
                        team_info = {
                            'id': team_data.get('id'),
                            'name': team_data.get('name'),
                            'slug': team_data.get('slug'),
                            'description': team_data.get('description'),
                            'privacy': team_data.get('privacy'),
                            'permission': team_data.get('permission')
                        }
                        all_teams.append(team_info)
                        
                    logger.info(f"Page {page}: Found {len(teams_data)} teams (total: {len(all_teams)})")
                    
                except (KeyError, ValueError, TypeError) as e:
                    logger.warning(f"Malformed team data in organization {org}: {e}")
                    continue
                
                # Check if there are more pages
                if len(teams_data) < params["per_page"]:
                    break
                    
                page += 1
            
            # Clear progress line and show final count
            if all_teams:
                print(f"\r   ✓ Loaded {len(all_teams)} teams from {page} page(s)              ")
            logger.info(f"Retrieved {len(all_teams)} teams for organization {org}")
            return all_teams
            
        except RateLimitError as e:
            logger.warning(f"🚨 Rate limit hit while fetching teams for {org}: {e}")
            self._handle_rate_limit(e.reset_time if hasattr(e, 'reset_time') else int(time.time()) + 3600)
            
            # Return empty list on rate limit to avoid blocking the scan
            logger.warning(f"Returning empty teams list for {org} due to rate limit")
            return []
            
        except (AuthenticationError, OrganizationNotFoundError):
            raise
        except Exception as e:
            log_exception(logger, f"Failed to get teams for organization {org}", e)
            return []  # Return empty instead of crashing

    def get_team_repos(
        self, org: str, team: str, etag: Optional[str] = None
    ) -> APIResponse:
        """Get repositories for a specific team.
        
        Args:
            org: Organization name
            team: Team slug
            etag: ETag for conditional requests
            
        Returns:
            APIResponse containing list of Repository objects
            
        Raises:
            TeamNotFoundError: If the team doesn't exist or is inaccessible
            OrganizationNotFoundError: If the organization doesn't exist
            AuthenticationError: If authentication fails
            NetworkError: If network operations fail
        """
        try:
            url = f"/orgs/{quote(org)}/teams/{quote(team)}/repos"
            params = {"per_page": 100}
            
            all_repos = []
            page = 1
            
            while True:
                params["page"] = page
                response = self._make_request("GET", url, etag=etag if page == 1 else None, params=params)
                
                if response.not_modified and page == 1:
                    return response
                    
                if not response.data:
                    # Empty response could mean team not found or no repos
                    if page == 1:
                        raise TeamNotFoundError(org, team)
                    break
                    
                repos_data = response.data
                if not repos_data:
                    break
                    
                try:
                    for repo_data in repos_data:
                        repo = Repository(
                            name=repo_data["name"],
                            full_name=repo_data["full_name"],
                            archived=repo_data.get("archived", False),
                            default_branch=repo_data.get("default_branch", "main"),
                            updated_at=datetime.fromisoformat(repo_data["updated_at"].replace("Z", "+00:00")),
                        )
                        all_repos.append(repo)
                except (KeyError, ValueError, TypeError) as e:
                    logger.warning(f"Malformed repository data for team {org}/{team}: {e}")
                    continue
                
                # Check if there are more pages
                if len(repos_data) < params["per_page"]:
                    break
                    
                page += 1
            
            logger.info(f"Retrieved {len(all_repos)} repositories for team {org}/{team}")
            
            return APIResponse(
                data=all_repos,
                etag=response.etag,
                not_modified=False,
                rate_limit_remaining=response.rate_limit_remaining,
                rate_limit_reset=response.rate_limit_reset,
            )
            
        except RateLimitError as e:
            # Handle rate limit gracefully for team repos
            logger.warning(f"🚨 Rate limit hit while fetching team repositories for {org}/{team}: {e}")
            self._handle_rate_limit(e.reset_time if hasattr(e, 'reset_time') else int(time.time()) + 3600)
            return APIResponse(data=[])  # Return empty instead of crashing
        except (TeamNotFoundError, OrganizationNotFoundError, AuthenticationError, NetworkError):
            raise
        except Exception as e:
            log_exception(logger, f"Failed to get repositories for team {org}/{team}", e)
            return APIResponse(data=[])  # Return empty instead of crashing

    def get_team_repositories(self, org: str, team: str) -> List[Dict[str, Any]]:
        """Get repositories for a specific team (wrapper for compatibility).
        
        Args:
            org: Organization name
            team: Team slug
            
        Returns:
            List of repository dictionaries
        """
        try:
            response = self.get_team_repos(org, team)
            # Convert Repository objects to dictionaries
            repos = []
            for repo in response.data:
                repos.append({
                    'name': repo.name,
                    'full_name': repo.full_name,
                    'archived': repo.archived,
                    'default_branch': repo.default_branch,
                    'updated_at': repo.updated_at.isoformat() if repo.updated_at else None
                })
            return repos
        except Exception as e:
            logger.warning(f"Error getting team repositories for {org}/{team}: {e}")
            return []

    def search_files(self, repo: Repository, patterns: List[str], fast_mode: bool = False) -> List[FileInfo]:
        """Search for files matching patterns in a repository using Code Search API with Tree API fallback.
        
        Args:
            repo: Repository to search in
            patterns: List of filename patterns to search for
            fast_mode: If True, only search root-level files
            
        Returns:
            List of FileInfo objects for matching files
            
        Raises:
            RepositoryNotFoundError: If the repository doesn't exist or is inaccessible
            NetworkError: If network operations fail
        """
        try:
            files = []
            
            # For large team scans, use Tree API first to avoid Code Search rate limits
            # This is much more efficient for scanning many repositories
            logger.debug(f"Using Tree API for {repo.full_name} (optimized for large scans)")
            return self._search_files_tree_api(repo, patterns, fast_mode)
            
        except RateLimitError as e:
            # Rate limit errors should be handled gracefully
            logger.warning(f"File search rate limited for {repo.full_name}: {e}")
            # Trigger rate limit handling
            self._handle_rate_limit(e.reset_time if hasattr(e, 'reset_time') else int(time.time()) + 3600)
            return []  # Return empty list instead of crashing
        except (RepositoryNotFoundError, NetworkError, AuthenticationError):
            raise
        except Exception as e:
            log_exception(logger, f"Failed to search files in repository {repo.full_name}", e)
            return []  # Return empty list instead of crashing to continue with other repos

    def _search_files_code_api(self, repo: Repository, patterns: List[str]) -> List[FileInfo]:
        """Search for files using GitHub Code Search API."""
        files = []
        
        try:
            for pattern in patterns:
                # Use GitHub Code Search API (has separate rate limits: 30 req/min)
                url = "/search/code"
                params = {
                    "q": f"filename:{pattern} repo:{repo.full_name}",
                    "per_page": 100,
                }
                
                page = 1
                while True:
                    params["page"] = page
                    
                    # Add extra delay for Code Search API due to lower limits
                    if page > 1:
                        time.sleep(2)  # 2 second delay between pages
                    
                    response = self._make_request("GET", url, params=params)
                    
                    if not response.data:
                        break
                        
                    search_data = response.data
                    items = search_data.get("items", [])
                    
                    if not items:
                        break
                        
                    try:
                        for item in items:
                            file_info = FileInfo(
                                path=item["path"],
                                sha=item["sha"],
                                size=item.get("size", 0),
                            )
                            files.append(file_info)
                    except (KeyError, TypeError) as e:
                        logger.warning(f"Malformed search result for pattern {pattern} in {repo.full_name}: {e}")
                        continue
                    
                    # Check if there are more pages
                    if len(items) < params["per_page"]:
                        break
                        
                    page += 1
            
            return files
            
        except RateLimitError as e:
            # Rate limit errors are expected and handled gracefully
            logger.warning(f"Code Search API rate limited for {repo.full_name}: {e}")
            raise
        except Exception as e:
            log_exception(logger, f"Code Search API error for {repo.full_name}", e)
            raise

    def _search_files_tree_api(self, repo: Repository, patterns: List[str], fast_mode: bool = False) -> List[FileInfo]:
        """Search for files using GitHub Tree API as fallback."""
        try:
            # Get the complete tree
            tree_response = self.get_tree(repo)
            if not tree_response.data:
                logger.debug(f"No tree data available for {repo.full_name} (likely empty repository)")
                return []
            
            all_files = tree_response.data
            matching_files = []
            
            for file_info in all_files:
                try:
                    # In fast mode, only check root-level files
                    if fast_mode and "/" in file_info.path:
                        continue
                        
                    # Intelligent filename-based matching (covers all locations)
                    filename = file_info.path.split("/")[-1]  # Get just the filename
                    
                    # Check if filename matches any of our target files
                    # This automatically covers ALL possible directory structures
                    if filename in patterns:
                        matching_files.append(file_info)
                        continue
                except (AttributeError, TypeError) as e:
                    logger.warning(f"Invalid file info in tree for {repo.full_name}: {e}")
                    continue
            
            return matching_files
            
        except RateLimitError as e:
            # Rate limit errors should be handled gracefully
            logger.warning(f"Tree API rate limited for {repo.full_name}: {e}")
            # Trigger rate limit handling
            self._handle_rate_limit(e.reset_time if hasattr(e, 'reset_time') else int(time.time()) + 3600)
            return []  # Return empty list instead of crashing
        except Exception as e:
            log_exception(logger, f"Tree API error for {repo.full_name}", e)
            return []  # Return empty list instead of crashing

    def _matches_pattern(self, filename: str, pattern: str) -> bool:
        """Check if a filename matches a pattern."""
        # Simple pattern matching - can be enhanced with glob patterns later
        if "*" in pattern:
            # Basic wildcard support
            import fnmatch
            return fnmatch.fnmatch(filename, pattern)
        else:
            # Exact match
            return filename == pattern
    
    def _create_filename_set(self, patterns: List[str]) -> set:
        """Create a set of filenames for O(1) lookup."""
        # Since we now use only filenames, convert list to set for fast lookup
        return set(patterns)
    
    def _path_pattern_match(self, full_path: str, patterns: List[str]) -> bool:
        """Check path patterns (slower, only used when filename match fails)."""
        import fnmatch
        
        for pattern in patterns:
            if "/" in pattern:  # Only check path patterns
                if pattern.startswith("*/") or pattern.startswith("**/"):
                    # Wildcard path pattern like */yarn.lock or **/yarn.lock
                    if fnmatch.fnmatch(full_path, pattern):
                        return True
                elif full_path.endswith("/" + pattern) or full_path == pattern:
                    # Exact path match like src/yarn.lock
                    return True
                else:
                    # Check if pattern matches any part of the path
                    if fnmatch.fnmatch(full_path, "*/" + pattern) or fnmatch.fnmatch(full_path, pattern):
                        return True
        
        return False
    
    def _matches_file_pattern(self, full_path: str, filename: str, pattern: str) -> bool:
        """Check if a file matches a pattern, supporting both filename and path patterns."""
        import fnmatch
        
        # If pattern contains a slash, it's a path pattern
        if "/" in pattern:
            # For path patterns, check if the full path ends with the pattern
            # or if the pattern matches the full path
            if pattern.startswith("*/") or pattern.startswith("**/"):
                # Wildcard path pattern like */yarn.lock or **/yarn.lock
                return fnmatch.fnmatch(full_path, pattern)
            elif full_path.endswith("/" + pattern) or full_path == pattern:
                # Exact path match like src/yarn.lock
                return True
            else:
                # Check if pattern matches any part of the path
                # For example, pattern "src/yarn.lock" should match "some/path/src/yarn.lock"
                return fnmatch.fnmatch(full_path, "*/" + pattern) or fnmatch.fnmatch(full_path, pattern)
        else:
            # For filename-only patterns, just match the filename
            return self._matches_pattern(filename, pattern)

    def get_file_content(
        self, repo: Repository, path: str, etag: Optional[str] = None
    ) -> APIResponse:
        """Get the content of a specific file.
        
        Args:
            repo: Repository containing the file
            path: Path to the file
            etag: ETag for conditional requests
            
        Returns:
            APIResponse containing FileContent object
            
        Raises:
            RepositoryNotFoundError: If the repository doesn't exist
            NetworkError: If network operations fail
        """
        try:
            url = f"/repos/{quote(repo.full_name)}/contents/{quote(path, safe='/')}"
            response = self._make_request("GET", url, etag=etag)
            
            if response.not_modified or not response.data:
                return response
                
            file_data = response.data
            
            # Handle directory responses
            if isinstance(file_data, list):
                logger.warning(f"Path {path} in {repo.full_name} is a directory, not a file")
                return APIResponse(data=None)
            
            # Validate required fields
            if not isinstance(file_data, dict):
                logger.warning(f"Invalid file data format for {repo.full_name}/{path}")
                return APIResponse(data=None)
            
            required_fields = ["content", "sha", "size"]
            missing_fields = [field for field in required_fields if field not in file_data]
            if missing_fields:
                logger.warning(f"Missing required fields {missing_fields} in file data for {repo.full_name}/{path}")
                return APIResponse(data=None)
            
            # Decode base64 content
            content_b64 = file_data.get("content", "")
            try:
                content = base64.b64decode(content_b64).decode("utf-8")
            except (ValueError, UnicodeDecodeError) as e:
                logger.warning(f"Failed to decode file content for {repo.full_name}/{path}: {e}")
                # Try with different encodings
                try:
                    content = base64.b64decode(content_b64).decode("utf-8", errors="replace")
                    logger.info(f"Decoded file content with replacement characters for {repo.full_name}/{path}")
                except Exception:
                    logger.error(f"Could not decode file content for {repo.full_name}/{path}")
                    return APIResponse(data=None)
            
            try:
                file_content = FileContent(
                    content=content,
                    sha=file_data["sha"],
                    size=file_data["size"],
                )
            except (KeyError, TypeError) as e:
                logger.warning(f"Failed to create FileContent object for {repo.full_name}/{path}: {e}")
                return APIResponse(data=None)
            
            return APIResponse(
                data=file_content,
                etag=response.etag,
                not_modified=False,
                rate_limit_remaining=response.rate_limit_remaining,
                rate_limit_reset=response.rate_limit_reset,
            )
            
        except (RepositoryNotFoundError, NetworkError, AuthenticationError):
            raise
        except Exception as e:
            log_exception(logger, f"Failed to get file content for {repo.full_name}/{path}", e)
            raise wrap_exception(e, f"Failed to get file content for {repo.full_name}/{path}")

    def get_multiple_file_contents(self, repo: Repository, file_paths: List[str]) -> Dict[str, 'FileContent']:
        """Get content for multiple files using GitHub's Tree API for better performance.
        
        This method uses the Git Tree API to get multiple files in fewer API calls,
        which is much more efficient than individual file content requests.
        
        Args:
            repo: Repository containing the files
            file_paths: List of file paths to fetch
            
        Returns:
            Dictionary mapping file paths to FileContent objects
        """
        if not file_paths:
            return {}
        
        try:
            # Get the repository tree
            tree_response = self.get_tree(repo)
            if not tree_response.data:
                return {}
            
            tree_files = tree_response.data
            
            # Create a mapping of path to tree entry
            tree_map = {file_info.path: file_info for file_info in tree_files}
            
            # Batch file content requests using Git Blob API
            file_contents = {}
            
            for file_path in file_paths:
                if file_path in tree_map:
                    file_info = tree_map[file_path]
                    try:
                        # Use Git Blob API to get file content by SHA
                        blob_content = self._get_blob_content(repo, file_info.sha)
                        if blob_content:
                            file_contents[file_path] = FileContent(
                                content=blob_content,
                                sha=file_info.sha,
                                size=file_info.size
                            )
                    except Exception as e:
                        logger.warning(f"Failed to get blob content for {repo.full_name}/{file_path}: {e}")
                        continue
            
            return file_contents
            
        except Exception as e:
            logger.warning(f"Batch file content fetch failed for {repo.full_name}: {e}")
            return {}
    
    def _get_blob_content(self, repo: Repository, sha: str) -> Optional[str]:
        """Get blob content by SHA using Git Blob API."""
        try:
            url = f"/repos/{quote(repo.full_name)}/git/blobs/{sha}"
            response = self._make_request("GET", url)
            
            if not response.data:
                return None
            
            blob_data = response.data
            content = blob_data.get('content', '')
            encoding = blob_data.get('encoding', 'base64')
            
            if encoding == 'base64':
                import base64
                try:
                    decoded_content = base64.b64decode(content).decode('utf-8')
                    return decoded_content
                except (UnicodeDecodeError, ValueError) as e:
                    logger.warning(f"Failed to decode blob {sha}: {e}")
                    return None
            else:
                # Assume it's already text
                return content
                
        except Exception as e:
            logger.warning(f"Failed to get blob content for SHA {sha}: {e}")
            return None

    def get_tree(self, repo: Repository, etag: Optional[str] = None) -> APIResponse:
        """Get the Git tree for a repository.
        
        Args:
            repo: Repository to get tree for
            etag: ETag for conditional requests
            
        Returns:
            APIResponse containing list of FileInfo objects
        """
        url = f"/repos/{quote(repo.full_name)}/git/trees/{repo.default_branch}"
        params = {"recursive": "1"}
        
        response = self._make_request("GET", url, etag=etag, params=params)
        
        if response.not_modified or not response.data:
            return response
            
        tree_data = response.data
        files = []
        
        for item in tree_data.get("tree", []):
            if item["type"] == "blob":  # Only include files, not directories
                file_info = FileInfo(
                    path=item["path"],
                    sha=item["sha"],
                    size=item.get("size", 0),
                )
                files.append(file_info)
        
        return APIResponse(
            data=files,
            etag=response.etag,
            not_modified=False,
            rate_limit_remaining=response.rate_limit_remaining,
            rate_limit_reset=response.rate_limit_reset,
        )
    
    async def _get_async_client(self) -> httpx.AsyncClient:
        """Get or create async HTTP client."""
        async with self._async_client_lock:
            if self._async_client is None or self._async_client.is_closed:
                self._async_client = httpx.AsyncClient(
                    base_url=self.BASE_URL,
                    headers={
                        "Authorization": f"Bearer {self.token}",
                        "Accept": "application/vnd.github.v3+json",
                        "User-Agent": "github-ioc-scanner/0.1.0",
                    },
                    timeout=30.0,
                    limits=httpx.Limits(
                        max_keepalive_connections=20,
                        max_connections=100,
                        keepalive_expiry=30.0
                    )
                )
            return self._async_client

    async def get_multiple_file_contents_async(
        self,
        repo: Repository,
        file_paths: List[str],
        max_concurrent: Optional[int] = None
    ) -> Dict[str, FileContent]:
        """Get multiple file contents with async parallel processing.
        
        Args:
            repo: Repository containing the files
            file_paths: List of file paths to fetch
            max_concurrent: Maximum concurrent requests
            
        Returns:
            Dictionary mapping file paths to FileContent objects
        """
        if not file_paths:
            return {}
        
        max_concurrent = max_concurrent or self.config.max_concurrent_requests
        semaphore = asyncio.Semaphore(max_concurrent)
        
        try:
            # Get the repository tree first
            tree_response = await self.get_tree_async(repo)
            if not tree_response.data:
                return {}
            
            tree_files = tree_response.data
            
            # Create a mapping of path to tree entry
            tree_map = {file_info.path: file_info for file_info in tree_files}
            
            # Create tasks for parallel blob fetching
            tasks = []
            for file_path in file_paths:
                if file_path in tree_map:
                    file_info = tree_map[file_path]
                    task = self._fetch_blob_async_with_semaphore(
                        semaphore, repo, file_path, file_info
                    )
                    tasks.append(task)
            
            # Execute all tasks in parallel
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            file_contents = {}
            for result in results:
                if isinstance(result, Exception):
                    logger.warning(f"Failed to fetch file content: {result}")
                    continue
                
                if result and len(result) == 2:
                    file_path, file_content = result
                    if file_content:
                        file_contents[file_path] = file_content
            
            return file_contents
            
        except Exception as e:
            logger.warning(f"Async parallel file content fetch failed for {repo.full_name}: {e}")
            return {}

    async def _fetch_blob_async_with_semaphore(
        self,
        semaphore: asyncio.Semaphore,
        repo: Repository,
        file_path: str,
        file_info: FileInfo
    ) -> Optional[tuple]:
        """Fetch a single blob with semaphore control."""
        async with semaphore:
            try:
                blob_content = await self._get_blob_content_async(repo, file_info.sha)
                if blob_content:
                    file_content = FileContent(
                        content=blob_content,
                        sha=file_info.sha,
                        size=file_info.size
                    )
                    return (file_path, file_content)
                return None
            except Exception as e:
                logger.warning(f"Failed to get blob content for {repo.full_name}/{file_path}: {e}")
                return None

    async def _get_blob_content_async(self, repo: Repository, sha: str) -> Optional[str]:
        """Get blob content by SHA using Git Blob API asynchronously."""
        try:
            url = f"/repos/{quote(repo.full_name)}/git/blobs/{sha}"
            response = await self._make_async_request("GET", url)
            
            if not response.data:
                return None
            
            blob_data = response.data
            content = blob_data.get('content', '')
            encoding = blob_data.get('encoding', 'base64')
            
            if encoding == 'base64':
                try:
                    decoded_content = base64.b64decode(content).decode('utf-8')
                    return decoded_content
                except (UnicodeDecodeError, ValueError) as e:
                    logger.warning(f"Failed to decode blob {sha}: {e}")
                    return None
            else:
                # Assume it's already text
                return content
                
        except Exception as e:
            logger.warning(f"Failed to get blob content for SHA {sha}: {e}")
            return None

    async def get_tree_async(self, repo: Repository, etag: Optional[str] = None) -> APIResponse:
        """Get the Git tree for a repository asynchronously.
        
        Args:
            repo: Repository to get tree for
            etag: ETag for conditional requests
            
        Returns:
            APIResponse containing list of FileInfo objects
        """
        url = f"/repos/{quote(repo.full_name)}/git/trees/{repo.default_branch}"
        params = {"recursive": "1"}
        
        response = await self._make_async_request("GET", url, etag=etag, params=params)
        
        if response.not_modified or not response.data:
            return response
            
        tree_data = response.data
        files = []
        
        for item in tree_data.get("tree", []):
            if item["type"] == "blob":  # Only include files, not directories
                file_info = FileInfo(
                    path=item["path"],
                    sha=item["sha"],
                    size=item.get("size", 0),
                )
                files.append(file_info)
        
        return APIResponse(
            data=files,
            etag=response.etag,
            not_modified=False,
            rate_limit_remaining=response.rate_limit_remaining,
            rate_limit_reset=response.rate_limit_reset,
        )

    async def _make_async_request(
        self, 
        method: str, 
        url: str, 
        etag: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> APIResponse:
        """Make an async request to the GitHub API with rate limiting and ETag support."""
        headers = kwargs.pop("headers", {})
        
        # Add ETag for conditional requests
        if etag:
            headers["If-None-Match"] = etag
            
        try:
            client = await self._get_async_client()
            response = await client.request(method, url, headers=headers, params=params, **kwargs)
            
            # Log rate limit information
            remaining = int(response.headers.get("X-RateLimit-Remaining", 0))
            reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
            log_rate_limit(logger, remaining, reset_time)
            
            # Proactive rate limit handling - slow down when approaching limits
            handle_smart_rate_limiting(remaining, reset_time)            
            # Handle rate limiting
            if response.status_code == 403:
                error_message = response.text.lower()
                if "rate limit exceeded" in error_message or "api rate limit exceeded" in error_message:
                    reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
                    raise RateLimitError(
                        f"GitHub API rate limit exceeded. {_format_reset_time(reset_time)}",
                        reset_time=reset_time
                    )
                elif "forbidden" in error_message:
                    raise AuthenticationError("Access forbidden. Check token permissions for this resource.")
                else:
                    raise APIError(f"Forbidden: {response.text}", status_code=403)
            
            # Handle 304 Not Modified
            if response.status_code == 304:
                logger.debug(f"Resource not modified: {url}")
                return APIResponse(
                    data=None,
                    etag=etag,
                    not_modified=True,
                    rate_limit_remaining=remaining,
                    rate_limit_reset=reset_time,
                )
            
            # Handle other HTTP errors
            response.raise_for_status()
            
            # Parse response data
            try:
                data = response.json() if response.content else None
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse JSON response from {url}: {e}")
                data = None
            
            return APIResponse(
                data=data,
                etag=response.headers.get("ETag"),
                not_modified=False,
                rate_limit_remaining=remaining,
                rate_limit_reset=reset_time,
            )
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Invalid GitHub token or insufficient permissions")
            elif e.response.status_code == 404:
                logger.debug(f"Resource not found: {url}")
                return APIResponse(data=None)
            elif e.response.status_code == 422:
                raise APIError(f"Unprocessable entity: {e.response.text}", status_code=422)
            else:
                raise APIError(f"HTTP {e.response.status_code}: {e.response.text}", status_code=e.response.status_code)
        except httpx.ConnectTimeout as e:
            raise NetworkError(f"Connection timeout to GitHub API: {url}", cause=e)
        except httpx.ReadTimeout as e:
            raise NetworkError(f"Read timeout from GitHub API: {url}", cause=e)
        except httpx.RequestError as e:
            raise NetworkError(f"Network error accessing GitHub API: {url}", cause=e)
        except (RateLimitError, AuthenticationError, APIError, NetworkError):
            # These are expected exceptions that should be re-raised as-is
            raise
        except Exception as e:
            log_exception(logger, f"Unexpected error making async request to {url}", e)
            raise wrap_exception(e, f"Unexpected error making async request to {url}")

    def close(self) -> None:
        """Close the HTTP client."""
        self.client.close()

    def get_sbom(self, repo: Repository) -> Optional[str]:
        """Download SBOM (Software Bill of Materials) from GitHub Dependency Graph API.
        
        Args:
            repo: Repository to get SBOM for
            
        Returns:
            SBOM content as JSON string, or None if not available
            
        Raises:
            RepositoryNotFoundError: If the repository doesn't exist
            NetworkError: If network operations fail
        """
        try:
            url = f"/repos/{quote(repo.full_name)}/dependency-graph/sbom"
            
            # Use specific Accept header for SBOM API
            headers = {
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28"
            }
            
            response = self._make_request("GET", url, headers=headers)
            
            if not response.data:
                logger.debug(f"No SBOM available for {repo.full_name}")
                return None
            
            # The SBOM API returns the SBOM directly as JSON
            sbom_data = response.data
            
            if isinstance(sbom_data, dict):
                # Convert to JSON string for consistent handling
                import json
                return json.dumps(sbom_data)
            elif isinstance(sbom_data, str):
                return sbom_data
            else:
                logger.warning(f"Unexpected SBOM data format for {repo.full_name}: {type(sbom_data)}")
                return None
                
        except RateLimitError as e:
            logger.warning(f"Rate limit hit while fetching SBOM for {repo.full_name}: {e}")
            raise
        except APIError as e:
            if e.status_code == 404:
                logger.debug(f"SBOM not available for {repo.full_name} (404)")
                return None
            elif e.status_code == 403:
                logger.warning(f"Access denied for SBOM in {repo.full_name} (403)")
                return None
            else:
                logger.warning(f"API error fetching SBOM for {repo.full_name}: {e}")
                return None
        except Exception as e:
            logger.warning(f"Failed to fetch SBOM for {repo.full_name}: {e}")
            return None

    async def aclose(self) -> None:
        """Close the async HTTP client."""
        if self._async_client and not self._async_client.is_closed:
            await self._async_client.aclose()
    
    def __enter__(self) -> "GitHubClient":
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.close()

    async def __aenter__(self) -> "GitHubClient":
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.aclose()