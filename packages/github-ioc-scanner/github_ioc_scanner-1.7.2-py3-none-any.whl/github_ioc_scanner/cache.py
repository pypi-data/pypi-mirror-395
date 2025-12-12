"""SQLite-based cache manager with ETag support for GitHub IOC Scanner."""

import json
import sqlite3
import hashlib
import platform
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timezone

from .exceptions import (
    CacheError,
    CacheInitializationError,
    CacheOperationError,
    wrap_exception
)
from .logging_config import get_logger, log_exception
from .models import (
    CacheStats, 
    PackageDependency, 
    IOCMatch, 
    Repository, 
    FileInfo
)

logger = get_logger(__name__)


class CacheManager:
    """SQLite-based cache manager with comprehensive caching and ETag support."""
    
    def __init__(self, cache_path: Optional[str] = None):
        """Initialize cache manager with cross-platform cache directory resolution."""
        try:
            if cache_path is None:
                cache_path = self._get_default_cache_path()
            
            self.cache_path = Path(cache_path)
            
            # Create cache directory if it doesn't exist
            try:
                self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            except (OSError, PermissionError) as e:
                raise CacheInitializationError(str(self.cache_path), cause=e)
            
            self.db_path = self.cache_path
            self._init_database()
            
            # Track cache statistics for current session
            self._session_stats = CacheStats()
            
            # Connection pool for better performance
            self._connection = None
            self._connection_lock = None
            
            # Connection pooling disabled for now
            self._connection = None
            self._connection_lock = None
            
            logger.debug(f"Cache initialized at {self.cache_path}")
            
        except CacheInitializationError:
            raise
        except Exception as e:
            log_exception(logger, f"Failed to initialize cache at {cache_path}", e)
            raise CacheInitializationError(str(cache_path), cause=e)
    
    def _get_default_cache_path(self) -> str:
        """Get platform-specific default cache directory path."""
        system = platform.system().lower()
        
        if system == "windows":
            local_app_data = Path.home() / "AppData" / "Local"
            cache_dir = local_app_data / "github-ioc-scan"
        else:
            cache_dir = Path.home() / ".cache" / "github-ioc-scan"
        
        return str(cache_dir / "cache.sqlite3")
    
    def _init_connection(self) -> None:
        """Initialize persistent database connection for better performance."""
        # Temporarily disable persistent connections due to threading issues
        # TODO: Re-enable with proper thread safety
        self._connection = None
        self._connection_lock = None
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection (persistent or new)."""
        if self._connection and self._connection_lock:
            return self._connection
        else:
            # Fallback to new connection
            conn = sqlite3.connect(self.db_path)
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("PRAGMA journal_mode = WAL")
            return conn
    
    def close(self) -> None:
        """Close persistent connection."""
        # Since we disabled persistent connections, this is a no-op
        pass
    
    def _init_database(self) -> None:
        """Initialize SQLite database with required schema."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Enable foreign keys and WAL mode for better performance
                conn.execute("PRAGMA foreign_keys = ON")
                conn.execute("PRAGMA journal_mode = WAL")
                
                conn.executescript("""
                    CREATE TABLE IF NOT EXISTS file_cache (
                        repo TEXT NOT NULL,
                        path TEXT NOT NULL,
                        sha TEXT NOT NULL,
                        content TEXT NOT NULL,
                        etag TEXT,
                        timestamp INTEGER NOT NULL,
                        PRIMARY KEY (repo, path, sha)
                    );
                    
                    CREATE TABLE IF NOT EXISTS parsed_packages (
                        repo TEXT NOT NULL,
                        path TEXT NOT NULL,
                        sha TEXT NOT NULL,
                        packages_json TEXT NOT NULL,
                        timestamp INTEGER NOT NULL,
                        PRIMARY KEY (repo, path, sha)
                    );
                    
                    CREATE TABLE IF NOT EXISTS scan_results (
                        repo TEXT NOT NULL,
                        path TEXT NOT NULL,
                        sha TEXT NOT NULL,
                        ioc_hash TEXT NOT NULL,
                        results_json TEXT NOT NULL,
                        timestamp INTEGER NOT NULL,
                        PRIMARY KEY (repo, path, sha, ioc_hash)
                    );
                    
                    CREATE TABLE IF NOT EXISTS repo_metadata (
                        org TEXT NOT NULL,
                        team TEXT NOT NULL DEFAULT '',
                        repos_json TEXT NOT NULL,
                        etag TEXT,
                        timestamp INTEGER NOT NULL,
                        PRIMARY KEY (org, team)
                    );
                    
                    CREATE TABLE IF NOT EXISTS etag_cache (
                        cache_key TEXT PRIMARY KEY,
                        etag TEXT NOT NULL,
                        timestamp INTEGER NOT NULL
                    );
                """)
                
                # Create indexes for better performance
                conn.executescript("""
                    CREATE INDEX IF NOT EXISTS idx_file_cache_repo_path ON file_cache(repo, path);
                    CREATE INDEX IF NOT EXISTS idx_parsed_packages_repo_path ON parsed_packages(repo, path);
                    CREATE INDEX IF NOT EXISTS idx_scan_results_repo_path ON scan_results(repo, path);
                    CREATE INDEX IF NOT EXISTS idx_repo_metadata_org ON repo_metadata(org);
                    CREATE INDEX IF NOT EXISTS idx_etag_cache_timestamp ON etag_cache(timestamp);
                    CREATE INDEX IF NOT EXISTS idx_etag_cache_key ON etag_cache(cache_key);
                """)
                
        except sqlite3.Error as e:
            raise CacheInitializationError(str(self.db_path), cause=e)
        except Exception as e:
            log_exception(logger, f"Unexpected error initializing database at {self.db_path}", e)
            raise CacheInitializationError(str(self.db_path), cause=e)
    
    def get_cache_stats(self) -> CacheStats:
        """Get comprehensive cache statistics."""
        with sqlite3.connect(self.db_path) as conn:
            # Get cache size information
            cursor = conn.execute("""
                SELECT 
                    (SELECT COUNT(*) FROM file_cache) as file_count,
                    (SELECT COUNT(*) FROM parsed_packages) as packages_count,
                    (SELECT COUNT(*) FROM scan_results) as results_count,
                    (SELECT COUNT(*) FROM repo_metadata) as repo_count,
                    (SELECT COUNT(*) FROM etag_cache) as etag_count
            """)
            counts = cursor.fetchone()
            
            total_cached_items = sum(counts) if counts else 0
            
            # Calculate estimated time saved (rough estimate: 100ms per API call avoided)
            estimated_time_saved = self._session_stats.hits * 0.1
            
            return CacheStats(
                hits=self._session_stats.hits,
                misses=self._session_stats.misses,
                time_saved=estimated_time_saved,
                cache_size=total_cached_items
            )
    
    def get_file_content(self, repo: str, path: str, sha: str) -> Optional[str]:
        """Get cached file content by repository, path, and SHA."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT content FROM file_cache WHERE repo = ? AND path = ? AND sha = ?",
                    (repo, path, sha)
                )
                result = cursor.fetchone()
                
                if result:
                    self._session_stats.hits += 1
                    return result[0]
                else:
                    self._session_stats.misses += 1
                    return None
                    
        except sqlite3.Error as e:
            logger.warning(f"Cache error getting file content for {repo}/{path}: {e}")
            self._session_stats.misses += 1
            return None
        except Exception as e:
            log_exception(logger, f"Unexpected error getting file content for {repo}/{path}", e)
            self._session_stats.misses += 1
            return None
    
    def store_file_content(self, repo: str, path: str, sha: str, content: str, etag: Optional[str] = None) -> None:
        """Store file content in cache."""
        try:
            timestamp = int(datetime.now(timezone.utc).timestamp())
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """INSERT OR REPLACE INTO file_cache 
                       (repo, path, sha, content, etag, timestamp) 
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (repo, path, sha, content, etag, timestamp)
                )
                
        except sqlite3.Error as e:
            logger.warning(f"Cache error storing file content for {repo}/{path}: {e}")
        except Exception as e:
            log_exception(logger, f"Unexpected error storing file content for {repo}/{path}", e)
    
    def get_parsed_packages(self, repo: str, path: str, sha: str) -> Optional[List[PackageDependency]]:
        """Get cached parsed packages for a file."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT packages_json FROM parsed_packages WHERE repo = ? AND path = ? AND sha = ?",
                    (repo, path, sha)
                )
                result = cursor.fetchone()
            
            if result:
                self._session_stats.hits += 1
                packages_data = json.loads(result[0])
                return [
                    PackageDependency(
                        name=pkg["name"],
                        version=pkg["version"],
                        dependency_type=pkg["dependency_type"]
                    )
                    for pkg in packages_data
                ]
            else:
                self._session_stats.misses += 1
                return None
        except Exception as e:
            logger.warning(f"Cache error getting parsed packages for {repo}/{path}: {e}")
            self._session_stats.misses += 1
            return None
    

    def store_parsed_packages(self, repo: str, path: str, sha: str, packages: List[PackageDependency]) -> None:
        """Store parsed packages in cache."""
        timestamp = int(datetime.now(timezone.utc).timestamp())
        packages_data = [
            {
                "name": pkg.name,
                "version": pkg.version,
                "dependency_type": pkg.dependency_type
            }
            for pkg in packages
        ]
        packages_json = json.dumps(packages_data)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT OR REPLACE INTO parsed_packages 
                   (repo, path, sha, packages_json, timestamp) 
                   VALUES (?, ?, ?, ?, ?)""",
                (repo, path, sha, packages_json, timestamp)
            )
    
    def get_scan_results(self, repo: str, path: str, sha: str, ioc_hash: str) -> Optional[List[IOCMatch]]:
        """Get cached IOC scan results."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT results_json FROM scan_results WHERE repo = ? AND path = ? AND sha = ? AND ioc_hash = ?",
                (repo, path, sha, ioc_hash)
            )
            result = cursor.fetchone()
            
            if result:
                self._session_stats.hits += 1
                results_data = json.loads(result[0])
                return [
                    IOCMatch(
                        repo=match["repo"],
                        file_path=match["file_path"],
                        package_name=match["package_name"],
                        version=match["version"],
                        ioc_source=match["ioc_source"]
                    )
                    for match in results_data
                ]
            else:
                self._session_stats.misses += 1
                return None
    
    def store_scan_results(self, repo: str, path: str, sha: str, ioc_hash: str, results: List[IOCMatch]) -> None:
        """Store IOC scan results in cache."""
        timestamp = int(datetime.now(timezone.utc).timestamp())
        results_data = [
            {
                "repo": match.repo,
                "file_path": match.file_path,
                "package_name": match.package_name,
                "version": match.version,
                "ioc_source": match.ioc_source
            }
            for match in results
        ]
        results_json = json.dumps(results_data)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT OR REPLACE INTO scan_results 
                   (repo, path, sha, ioc_hash, results_json, timestamp) 
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (repo, path, sha, ioc_hash, results_json, timestamp)
            )
    
    def get_repository_metadata(self, org: str, team: str = "") -> Optional[Tuple[List[Repository], Optional[str], Optional[datetime]]]:
        """Get cached repository metadata for organization or team.
        
        Returns:
            Tuple of (repositories, etag, cache_timestamp) or None if not cached
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT repos_json, etag, timestamp FROM repo_metadata WHERE org = ? AND team = ?",
                (org, team)
            )
            result = cursor.fetchone()
            
            if result:
                self._session_stats.hits += 1
                repos_data = json.loads(result[0])
                repositories = [
                    Repository(
                        name=repo["name"],
                        full_name=repo["full_name"],
                        archived=repo["archived"],
                        default_branch=repo["default_branch"],
                        updated_at=datetime.fromisoformat(repo["updated_at"])
                    )
                    for repo in repos_data
                ]
                # Convert timestamp to datetime
                cache_timestamp = datetime.fromtimestamp(result[2], tz=timezone.utc) if result[2] else None
                return repositories, result[1], cache_timestamp
            else:
                self._session_stats.misses += 1
                return None
    
    def store_repository_metadata(self, org: str, repos: List[Repository], etag: Optional[str] = None, team: str = "") -> None:
        """Store repository metadata in cache."""
        timestamp = int(datetime.now(timezone.utc).timestamp())
        repos_data = [
            {
                "name": repo.name,
                "full_name": repo.full_name,
                "archived": repo.archived,
                "default_branch": repo.default_branch,
                "updated_at": repo.updated_at.isoformat()
            }
            for repo in repos
        ]
        repos_json = json.dumps(repos_data)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT OR REPLACE INTO repo_metadata 
                   (org, team, repos_json, etag, timestamp) 
                   VALUES (?, ?, ?, ?, ?)""",
                (org, team, repos_json, etag, timestamp)
            )
    
    def get_etag(self, cache_key: str) -> Optional[str]:
        """Get cached ETag for a given cache key."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT etag FROM etag_cache WHERE cache_key = ?",
                (cache_key,)
            )
            result = cursor.fetchone()
            
            if result:
                self._session_stats.hits += 1
                return result[0]
            else:
                self._session_stats.misses += 1
                return None
    
    def store_etag(self, cache_key: str, etag: str) -> None:
        """Store ETag for a given cache key."""
        timestamp = int(datetime.now(timezone.utc).timestamp())
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """INSERT OR REPLACE INTO etag_cache 
                   (cache_key, etag, timestamp) 
                   VALUES (?, ?, ?)""",
                (cache_key, etag, timestamp)
            )
    
    def clear_cache(self, cache_type: Optional[str] = None) -> None:
        """Clear cache data."""
        with sqlite3.connect(self.db_path) as conn:
            if cache_type == "file":
                conn.execute("DELETE FROM file_cache")
            elif cache_type == "packages":
                conn.execute("DELETE FROM parsed_packages")
            elif cache_type == "results":
                conn.execute("DELETE FROM scan_results")
            elif cache_type == "repos":
                conn.execute("DELETE FROM repo_metadata")
            elif cache_type == "etags":
                conn.execute("DELETE FROM etag_cache")
            elif cache_type is None:
                conn.executescript("""
                    DELETE FROM file_cache;
                    DELETE FROM parsed_packages;
                    DELETE FROM scan_results;
                    DELETE FROM repo_metadata;
                    DELETE FROM etag_cache;
                """)
            else:
                raise ValueError(f"Unknown cache type: {cache_type}")
    
    def refresh_repository_cache(self, org: str, team: str = "") -> None:
        """Refresh cached repository metadata for a specific org/team."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "DELETE FROM repo_metadata WHERE org = ? AND team = ?",
                (org, team)
            )

    def refresh_repository_files(self, repo_name: str) -> int:
        """Refresh all cached data for a specific repository.
        
        Args:
            repo_name: Repository name in format 'org/repo'
            
        Returns:
            Number of cache entries removed
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Count entries before deletion
                cursor = conn.execute("""
                    SELECT 
                        (SELECT COUNT(*) FROM file_cache WHERE repo = ?) +
                        (SELECT COUNT(*) FROM parsed_packages WHERE repo = ?) +
                        (SELECT COUNT(*) FROM scan_results WHERE repo = ?)
                """, (repo_name, repo_name, repo_name))
                
                total_removed = cursor.fetchone()[0]
                
                # Remove all cached data for this repository
                conn.execute("DELETE FROM file_cache WHERE repo = ?", (repo_name,))
                conn.execute("DELETE FROM parsed_packages WHERE repo = ?", (repo_name,))
                conn.execute("DELETE FROM scan_results WHERE repo = ?", (repo_name,))
                
                # Also remove ETags related to this repository
                conn.execute("DELETE FROM etag_cache WHERE cache_key LIKE ?", (f"file:{repo_name}/%",))
                
                logger.info(f"Refreshed cache for repository {repo_name}: removed {total_removed} entries")
                return total_removed
                
        except sqlite3.Error as e:
            logger.warning(f"Error refreshing cache for repository {repo_name}: {e}")
            return 0
        except Exception as e:
            log_exception(logger, f"Unexpected error refreshing cache for repository {repo_name}", e)
            return 0
    
    def cleanup_old_entries(self, days_old: int = 30) -> int:
        """Clean up cache entries older than specified days."""
        cutoff_timestamp = int((datetime.now(timezone.utc).timestamp() - (days_old * 24 * 3600)))
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT 
                    (SELECT COUNT(*) FROM file_cache WHERE timestamp < ?) +
                    (SELECT COUNT(*) FROM parsed_packages WHERE timestamp < ?) +
                    (SELECT COUNT(*) FROM scan_results WHERE timestamp < ?) +
                    (SELECT COUNT(*) FROM repo_metadata WHERE timestamp < ?) +
                    (SELECT COUNT(*) FROM etag_cache WHERE timestamp < ?)
            """, (cutoff_timestamp,) * 5)
            
            total_removed = cursor.fetchone()[0]
            
            conn.executescript(f"""
                DELETE FROM file_cache WHERE timestamp < {cutoff_timestamp};
                DELETE FROM parsed_packages WHERE timestamp < {cutoff_timestamp};
                DELETE FROM scan_results WHERE timestamp < {cutoff_timestamp};
                DELETE FROM repo_metadata WHERE timestamp < {cutoff_timestamp};
                DELETE FROM etag_cache WHERE timestamp < {cutoff_timestamp};
            """)
            
            return total_removed
    
    def get_cache_info(self) -> Dict[str, int]:
        """Get detailed information about cache contents."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT 
                    'file_cache' as table_name, COUNT(*) as count FROM file_cache
                UNION ALL
                SELECT 
                    'parsed_packages' as table_name, COUNT(*) as count FROM parsed_packages
                UNION ALL
                SELECT 
                    'scan_results' as table_name, COUNT(*) as count FROM scan_results
                UNION ALL
                SELECT 
                    'repo_metadata' as table_name, COUNT(*) as count FROM repo_metadata
                UNION ALL
                SELECT 
                    'etag_cache' as table_name, COUNT(*) as count FROM etag_cache
            """)
            
            cache_info = {}
            for row in cursor.fetchall():
                cache_info[row[0]] = row[1]
            
            try:
                cache_info['db_size_bytes'] = self.db_path.stat().st_size
            except (OSError, AttributeError):
                cache_info['db_size_bytes'] = 0
            
            # Add cache path information
            cache_info['cache_path'] = str(self.cache_path)
            
            return cache_info

    def get_detailed_cache_info(self) -> Dict[str, object]:
        """Get comprehensive cache information including repository breakdown."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Basic counts
                basic_info = self.get_cache_info()
                
                # Repository breakdown
                cursor = conn.execute("""
                    SELECT repo, COUNT(*) as file_count 
                    FROM file_cache 
                    GROUP BY repo 
                    ORDER BY file_count DESC 
                    LIMIT 10
                """)
                top_repos = [{"repo": row[0], "files": row[1]} for row in cursor.fetchall()]
                
                # Age information
                cursor = conn.execute("""
                    SELECT 
                        MIN(timestamp) as oldest,
                        MAX(timestamp) as newest,
                        AVG(timestamp) as average
                    FROM (
                        SELECT timestamp FROM file_cache
                        UNION ALL
                        SELECT timestamp FROM parsed_packages
                        UNION ALL
                        SELECT timestamp FROM scan_results
                        UNION ALL
                        SELECT timestamp FROM repo_metadata
                        UNION ALL
                        SELECT timestamp FROM etag_cache
                    )
                """)
                age_info = cursor.fetchone()
                
                detailed_info = {
                    **basic_info,
                    "top_repositories": top_repos,
                    "cache_age": {
                        "oldest_entry": datetime.fromtimestamp(age_info[0], tz=timezone.utc).isoformat() if age_info[0] else None,
                        "newest_entry": datetime.fromtimestamp(age_info[1], tz=timezone.utc).isoformat() if age_info[1] else None,
                        "average_age_days": (datetime.now(timezone.utc).timestamp() - age_info[2]) / 86400 if age_info[2] else None
                    }
                }
                
                return detailed_info
                
        except sqlite3.Error as e:
            logger.warning(f"Error getting detailed cache info: {e}")
            return self.get_cache_info()
        except Exception as e:
            log_exception(logger, "Unexpected error getting detailed cache info", e)
            return self.get_cache_info()
    
    def generate_ioc_hash(self, ioc_definitions: Dict[str, Dict]) -> str:
        """Generate a hash for IOC definitions to use for cache invalidation."""
        ioc_str = json.dumps(ioc_definitions, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(ioc_str.encode('utf-8')).hexdigest()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        pass
