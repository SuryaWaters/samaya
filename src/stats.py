#!/usr/bin/env python3

import json
from datetime import datetime
from pathlib import Path
from .constants import STATS_DIR_NAME, STATS_FILE_NAME, MAX_STORED_SESSIONS, STATS_EMOJI


class SessionStats:
    """Handle session statistics and tracking"""
    
    def __init__(self):
        self.stats_dir = Path.home() / STATS_DIR_NAME
        self.stats_file = self.stats_dir / STATS_FILE_NAME
        self._ensure_stats_dir()
    
    def _ensure_stats_dir(self):
        """Create stats directory if it doesn't exist"""
        self.stats_dir.mkdir(exist_ok=True)
    
    def _load_stats(self):
        """Load existing stats or create new ones"""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                # If file is corrupted, start fresh
                pass
        
        return {
            'total_sessions': 0,
            'sessions_by_type': {
                'short': 0,
                'medium': 0, 
                'long': 0,
                'custom': 0
            },
            'total_minutes': 0,
            'sessions': []
        }
    
    def _save_stats(self, stats):
        """Save stats to file"""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(stats, f, indent=2)
        except IOError:
            # Silently fail if we can't write stats
            pass
    
    def log_session(self, session_type, duration_minutes, completed=True):
        """Log a completed session"""
        stats = self._load_stats()
        
        # Update counters
        stats['total_sessions'] += 1
        if session_type in stats['sessions_by_type']:
            stats['sessions_by_type'][session_type] += 1
        else:
            stats['sessions_by_type']['custom'] += 1
        
        if completed:
            stats['total_minutes'] += duration_minutes
        
        # Log individual session
        session_record = {
            'timestamp': datetime.now().isoformat(),
            'type': session_type,
            'duration': duration_minutes,
            'completed': completed
        }
        stats['sessions'].append(session_record)
        
        # Keep only last MAX_STORED_SESSIONS to avoid file bloat
        if len(stats['sessions']) > MAX_STORED_SESSIONS:
            stats['sessions'] = stats['sessions'][-MAX_STORED_SESSIONS:]
        
        self._save_stats(stats)
    
    def get_summary(self):
        """Get session summary statistics"""
        stats = self._load_stats()
        return {
            'total_sessions': stats['total_sessions'],
            'total_minutes': stats['total_minutes'],
            'sessions_by_type': stats['sessions_by_type'],
            'total_hours': round(stats['total_minutes'] / 60, 1)
        }
    
    def clear_stats(self):
        """Clear all session statistics"""
        try:
            if self.stats_file.exists():
                self.stats_file.unlink()
            print("✅ All session statistics have been cleared.")
        except OSError:
            print("❌ Failed to clear statistics file.")
    
    def display_stats(self):
        """Display formatted session statistics"""
        summary = self.get_summary()
        
        print(f"\n{STATS_EMOJI} Session Statistics")
        print("=" * 25)
        print(f"Total Sessions: {summary['total_sessions']}")
        print(f"Total Time: {summary['total_minutes']} minutes ({summary['total_hours']} hours)")
        print()
        print("Sessions by Type:")
        for session_type, count in summary['sessions_by_type'].items():
            if count > 0:
                print(f"  {session_type.capitalize()}: {count}")
        print()