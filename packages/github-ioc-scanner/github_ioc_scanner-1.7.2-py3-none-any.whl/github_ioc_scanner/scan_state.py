"""Scan state management for resumable scans."""

import json
import os
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import logging

from .models import IOCMatch, Repository

logger = logging.getLogger(__name__)


@dataclass
class ScanState:
    """Represents the state of a scan for resumability."""
    scan_id: str
    org: str
    scan_type: str  # 'team-first-org', 'org', 'team', 'repo'
    target: str  # team name, repo name, or org name
    start_time: float
    last_update: float
    
    # Scan configuration
    config: Dict[str, Any]
    
    # Progress tracking
    total_repositories: int
    total_teams: Optional[int] = None
    
    # Completed items
    completed_repositories: List[str] = None
    completed_teams: List[str] = None
    
    # Current progress
    current_team_index: Optional[int] = None
    current_team_name: Optional[str] = None
    
    # Results so far
    matches: List[Dict[str, Any]] = None
    files_scanned: int = 0
    repositories_scanned: int = 0
    
    # Error tracking
    failed_repositories: List[Dict[str, str]] = None
    
    def __post_init__(self):
        if self.completed_repositories is None:
            self.completed_repositories = []
        if self.completed_teams is None:
            self.completed_teams = []
        if self.matches is None:
            self.matches = []
        if self.failed_repositories is None:
            self.failed_repositories = []


class ScanStateManager:
    """Manages scan state persistence and recovery."""
    
    def __init__(self, state_dir: Optional[str] = None):
        """Initialize scan state manager.
        
        Args:
            state_dir: Directory to store scan state files
        """
        if state_dir:
            self.state_dir = Path(state_dir)
        else:
            # Default to ~/.cache/github-ioc-scanner/scan-states
            cache_dir = os.getenv('GITHUB_IOC_CACHE_DIR', '~/.cache/github-ioc-scanner')
            self.state_dir = Path(cache_dir).expanduser() / 'scan-states'
        
        self.state_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Scan state directory: {self.state_dir}")
    
    def create_scan_state(self, org: str, scan_type: str, target: str, config: Dict[str, Any]) -> ScanState:
        """Create a new scan state.
        
        Args:
            org: Organization name
            scan_type: Type of scan ('team-first-org', 'org', 'team', 'repo')
            target: Target name (team, repo, or org)
            config: Scan configuration
            
        Returns:
            New ScanState instance
        """
        scan_id = f"{org}_{scan_type}_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        
        state = ScanState(
            scan_id=scan_id,
            org=org,
            scan_type=scan_type,
            target=target,
            start_time=time.time(),
            last_update=time.time(),
            config=config,
            total_repositories=0
        )
        
        logger.info(f"Created scan state: {scan_id}")
        return state
    
    def save_state(self, state: ScanState) -> None:
        """Save scan state to disk.
        
        Args:
            state: ScanState to save
        """
        state.last_update = time.time()
        
        state_file = self.state_dir / f"{state.scan_id}.json"
        
        try:
            # Convert IOCMatch objects to dicts for JSON serialization
            serializable_state = asdict(state)
            
            with open(state_file, 'w') as f:
                json.dump(serializable_state, f, indent=2, default=str)
            
            logger.debug(f"Saved scan state: {state.scan_id}")
            
        except Exception as e:
            logger.error(f"Failed to save scan state {state.scan_id}: {e}")
    
    def load_state(self, scan_id: str) -> Optional[ScanState]:
        """Load scan state from disk.
        
        Args:
            scan_id: Scan ID to load
            
        Returns:
            ScanState if found, None otherwise
        """
        state_file = self.state_dir / f"{scan_id}.json"
        
        if not state_file.exists():
            logger.warning(f"Scan state file not found: {scan_id}")
            return None
        
        try:
            with open(state_file, 'r') as f:
                data = json.load(f)
            
            # Convert back to ScanState
            state = ScanState(**data)
            
            logger.info(f"Loaded scan state: {scan_id}")
            return state
            
        except Exception as e:
            logger.error(f"Failed to load scan state {scan_id}: {e}")
            return None
    
    def list_scan_states(self) -> List[Dict[str, Any]]:
        """List all available scan states.
        
        Returns:
            List of scan state summaries
        """
        states = []
        
        for state_file in self.state_dir.glob("*.json"):
            try:
                with open(state_file, 'r') as f:
                    data = json.load(f)
                
                # Create summary
                summary = {
                    'scan_id': data['scan_id'],
                    'org': data['org'],
                    'scan_type': data['scan_type'],
                    'target': data['target'],
                    'start_time': data['start_time'],
                    'last_update': data['last_update'],
                    'progress': f"{data['repositories_scanned']}/{data['total_repositories']} repos",
                    'age_hours': (time.time() - data['last_update']) / 3600
                }
                
                states.append(summary)
                
            except Exception as e:
                logger.warning(f"Failed to read state file {state_file}: {e}")
        
        # Sort by last update (newest first)
        states.sort(key=lambda x: x['last_update'], reverse=True)
        
        return states
    
    def delete_state(self, scan_id: str) -> bool:
        """Delete a scan state.
        
        Args:
            scan_id: Scan ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        state_file = self.state_dir / f"{scan_id}.json"
        
        if state_file.exists():
            try:
                state_file.unlink()
                logger.info(f"Deleted scan state: {scan_id}")
                return True
            except Exception as e:
                logger.error(f"Failed to delete scan state {scan_id}: {e}")
                return False
        else:
            logger.warning(f"Scan state not found for deletion: {scan_id}")
            return False
    
    def cleanup_old_states(self, max_age_days: int = 7) -> int:
        """Clean up old scan states.
        
        Args:
            max_age_days: Maximum age in days before cleanup
            
        Returns:
            Number of states cleaned up
        """
        cutoff_time = time.time() - (max_age_days * 24 * 3600)
        cleaned = 0
        
        for state_file in self.state_dir.glob("*.json"):
            try:
                with open(state_file, 'r') as f:
                    data = json.load(f)
                
                if data.get('last_update', 0) < cutoff_time:
                    state_file.unlink()
                    cleaned += 1
                    logger.debug(f"Cleaned up old scan state: {data.get('scan_id', 'unknown')}")
                    
            except Exception as e:
                logger.warning(f"Failed to process state file {state_file}: {e}")
        
        if cleaned > 0:
            logger.info(f"Cleaned up {cleaned} old scan states")
        
        return cleaned
    
    def cleanup_completed_scan(self, scan_id: str) -> bool:
        """Clean up a completed scan state.
        
        Args:
            scan_id: Scan ID to clean up
            
        Returns:
            True if cleaned up successfully, False otherwise
        """
        return self.delete_state(scan_id)
    
    def get_resumable_scans(self, org: str, scan_type: str) -> List[Dict[str, Any]]:
        """Get resumable scans for a specific org and type.
        
        Args:
            org: Organization name
            scan_type: Scan type to filter by
            
        Returns:
            List of matching scan summaries
        """
        all_states = self.list_scan_states()
        
        resumable = [
            state for state in all_states
            if state['org'] == org and state['scan_type'] == scan_type
            and state['age_hours'] < 24  # Only show scans from last 24 hours
        ]
        
        return resumable


def add_ioc_match_to_state(state: ScanState, match: IOCMatch) -> None:
    """Add an IOC match to the scan state.
    
    Args:
        state: ScanState to update
        match: IOCMatch to add
    """
    match_dict = {
        'repo': match.repo,
        'file_path': match.file_path,
        'package_name': match.package_name,
        'version': match.version,
        'ioc_source': match.ioc_source
    }
    
    state.matches.append(match_dict)


def convert_state_matches_to_ioc_matches(matches_data: List[Dict[str, Any]]) -> List[IOCMatch]:
    """Convert state matches back to IOCMatch objects.
    
    Args:
        matches_data: List of match dictionaries from scan state
        
    Returns:
        List of IOCMatch objects
    """
    matches = []
    
    if not matches_data:
        return matches
    
    for match_dict in matches_data:
        try:
            match = IOCMatch(
                repo=match_dict['repo'],
                file_path=match_dict['file_path'],
                package_name=match_dict['package_name'],
                version=match_dict['version'],
                ioc_source=match_dict['ioc_source']
            )
            matches.append(match)
        except KeyError as e:
            logger.warning(f"Invalid match data in scan state, missing field: {e}")
            continue
    
    return matches