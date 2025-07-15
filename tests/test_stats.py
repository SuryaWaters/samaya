#!/usr/bin/env python3

import unittest
import tempfile
import os
import sys
from pathlib import Path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.stats import SessionStats


class TestSessionStats(unittest.TestCase):
    
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.stats = SessionStats()
        # Override the stats directory for testing
        self.stats.stats_dir = Path(self.test_dir)
        self.stats.stats_file = self.stats.stats_dir / 'stats.json'
    
    def tearDown(self):
        # Clean up temporary files
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_initial_stats(self):
        """Test initial stats are empty"""
        summary = self.stats.get_summary()
        self.assertEqual(summary['total_sessions'], 0)
        self.assertEqual(summary['total_minutes'], 0)
        self.assertEqual(summary['total_hours'], 0)
    
    def test_log_completed_session(self):
        """Test logging a completed session"""
        self.stats.log_session('short', 5, completed=True)
        summary = self.stats.get_summary()
        
        self.assertEqual(summary['total_sessions'], 1)
        self.assertEqual(summary['total_minutes'], 5)
        self.assertEqual(summary['sessions_by_type']['short'], 1)
    
    def test_log_incomplete_session(self):
        """Test logging an incomplete session"""
        self.stats.log_session('medium', 15, completed=False)
        summary = self.stats.get_summary()
        
        self.assertEqual(summary['total_sessions'], 1)
        self.assertEqual(summary['total_minutes'], 0)  # Not added for incomplete
        self.assertEqual(summary['sessions_by_type']['medium'], 1)
    
    def test_custom_session_logging(self):
        """Test logging custom sessions"""
        self.stats.log_session('custom', 10, completed=True)
        summary = self.stats.get_summary()
        
        self.assertEqual(summary['total_sessions'], 1)
        self.assertEqual(summary['sessions_by_type']['custom'], 1)
    
    def test_multiple_sessions(self):
        """Test logging multiple sessions"""
        self.stats.log_session('short', 5, completed=True)
        self.stats.log_session('medium', 15, completed=True)
        self.stats.log_session('long', 25, completed=False)
        
        summary = self.stats.get_summary()
        
        self.assertEqual(summary['total_sessions'], 3)
        self.assertEqual(summary['total_minutes'], 20)  # 5 + 15 (incomplete not counted)
        self.assertEqual(summary['sessions_by_type']['short'], 1)
        self.assertEqual(summary['sessions_by_type']['medium'], 1)
        self.assertEqual(summary['sessions_by_type']['long'], 1)
    
    def test_display_stats_no_crash(self):
        """Test that display_stats doesn't crash"""
        try:
            self.stats.display_stats()
        except Exception as e:
            self.fail(f"display_stats() raised an exception: {e}")
    
    def test_clear_stats(self):
        """Test clearing statistics"""
        # Add some stats first
        self.stats.log_session('short', 5, completed=True)
        self.stats.log_session('medium', 15, completed=True)
        
        # Verify stats exist
        summary = self.stats.get_summary()
        self.assertEqual(summary['total_sessions'], 2)
        self.assertEqual(summary['total_minutes'], 20)
        
        # Clear stats
        self.stats.clear_stats()
        
        # Verify stats are cleared
        summary = self.stats.get_summary()
        self.assertEqual(summary['total_sessions'], 0)
        self.assertEqual(summary['total_minutes'], 0)
        
        # Verify file is deleted
        self.assertFalse(self.stats.stats_file.exists())
    
    def test_clear_stats_no_file(self):
        """Test clearing stats when no file exists"""
        # Ensure no file exists
        self.assertFalse(self.stats.stats_file.exists())
        
        # Should not crash
        try:
            self.stats.clear_stats()
        except Exception as e:
            self.fail(f"clear_stats() raised an exception: {e}")


if __name__ == '__main__':
    unittest.main()