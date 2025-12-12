"""CLI functions for scan resume functionality."""

import time
from datetime import datetime
from typing import List, Dict, Any

from .scan_state import ScanStateManager


def list_resumable_scans() -> None:
    """List all resumable scans."""
    
    print("📋 Available Resumable Scans")
    print("=" * 50)
    
    state_manager = ScanStateManager()
    states = state_manager.list_scan_states()
    
    if not states:
        print("No resumable scans found.")
        print("\n💡 Tip: Run a scan with --save-state to create resumable checkpoints")
        return
    
    print(f"Found {len(states)} scan(s):\n")
    
    for i, state in enumerate(states, 1):
        age_hours = state['age_hours']
        start_time = datetime.fromtimestamp(state['start_time'])
        last_update = datetime.fromtimestamp(state['last_update'])
        
        print(f"{i:2d}. Scan ID: {state['scan_id']}")
        print(f"    Organization: {state['org']}")
        print(f"    Type: {state['scan_type']}")
        print(f"    Target: {state['target']}")
        print(f"    Progress: {state['progress']}")
        print(f"    Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"    Last Update: {last_update.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if age_hours < 1:
            age_str = f"{age_hours * 60:.0f} minutes ago"
        elif age_hours < 24:
            age_str = f"{age_hours:.1f} hours ago"
        else:
            age_str = f"{age_hours / 24:.1f} days ago"
        
        print(f"    Age: {age_str}")
        
        # Show resume command
        print(f"    Resume: --resume {state['scan_id']}")
        print()
    
    print("💡 Usage:")
    print("  python3 -m github_ioc_scanner.cli --resume <SCAN_ID>")
    print("  python3 -m github_ioc_scanner.cli --list-scans  # Show this list")


def show_resume_info(scan_id: str) -> bool:
    """Show information about a resumable scan.
    
    Args:
        scan_id: Scan ID to show info for
        
    Returns:
        True if scan found, False otherwise
    """
    
    state_manager = ScanStateManager()
    state = state_manager.load_state(scan_id)
    
    if not state:
        print(f"❌ Scan not found: {scan_id}")
        print("\n💡 Use --list-scans to see available scans")
        return False
    
    print(f"📋 Scan Information: {scan_id}")
    print("=" * 60)
    
    start_time = datetime.fromtimestamp(state.start_time)
    last_update = datetime.fromtimestamp(state.last_update)
    
    print(f"Organization: {state.org}")
    print(f"Scan Type: {state.scan_type}")
    print(f"Target: {state.target}")
    print(f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Last Update: {last_update.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Progress information
    if state.total_repositories:
        progress_pct = (state.repositories_scanned / state.total_repositories) * 100
        print(f"Progress: {state.repositories_scanned}/{state.total_repositories} repositories ({progress_pct:.1f}%)")
    
    if state.total_teams:
        team_progress = len(state.completed_teams) if state.completed_teams else 0
        team_pct = (team_progress / state.total_teams) * 100
        print(f"Teams: {team_progress}/{state.total_teams} completed ({team_pct:.1f}%)")
    
    if state.current_team_name:
        print(f"Current Team: {state.current_team_name} (index {state.current_team_index})")
    
    # Results so far
    threat_count = len(state.matches) if state.matches else 0
    print(f"Threats Found: {threat_count}")
    print(f"Files Scanned: {state.files_scanned}")
    
    # Failed repositories
    if state.failed_repositories:
        print(f"Failed Repositories: {len(state.failed_repositories)}")
    
    # Configuration
    print(f"\nConfiguration:")
    for key, value in state.config.items():
        print(f"  {key}: {value}")
    
    print(f"\n🚀 To resume this scan:")
    print(f"  python3 -m github_ioc_scanner.cli --resume {scan_id}")
    
    return True


def cleanup_old_scans(max_age_days: int = 7) -> None:
    """Clean up old scan states.
    
    Args:
        max_age_days: Maximum age in days before cleanup
    """
    
    print(f"🧹 Cleaning up scan states older than {max_age_days} days...")
    
    state_manager = ScanStateManager()
    cleaned = state_manager.cleanup_old_states(max_age_days)
    
    if cleaned > 0:
        print(f"✅ Cleaned up {cleaned} old scan state(s)")
    else:
        print("✅ No old scan states to clean up")


def get_resumable_scans_for_config(org: str, scan_type: str) -> List[Dict[str, Any]]:
    """Get resumable scans matching the current configuration.
    
    Args:
        org: Organization name
        scan_type: Scan type
        
    Returns:
        List of matching resumable scans
    """
    
    state_manager = ScanStateManager()
    return state_manager.get_resumable_scans(org, scan_type)


def suggest_resume_if_available(org: str, scan_type: str) -> None:
    """Suggest resuming if there are available scans.
    
    Args:
        org: Organization name
        scan_type: Scan type
    """
    
    resumable = get_resumable_scans_for_config(org, scan_type)
    
    if resumable:
        print(f"\n💡 Found {len(resumable)} resumable scan(s) for {org} ({scan_type}):")
        
        for scan in resumable[:3]:  # Show up to 3 most recent
            age_hours = scan['age_hours']
            if age_hours < 1:
                age_str = f"{age_hours * 60:.0f}m ago"
            else:
                age_str = f"{age_hours:.1f}h ago"
            
            print(f"  • {scan['scan_id']} - {scan['progress']} ({age_str})")
        
        if len(resumable) > 3:
            print(f"  ... and {len(resumable) - 3} more")
        
        print(f"\n🔄 To resume: --resume <SCAN_ID>")
        print(f"📋 To list all: --list-scans")
        print(f"⏭️  To start new scan anyway, continue...")
        
        # Give user a moment to see the suggestion
        import time
        time.sleep(2)