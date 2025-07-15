#!/usr/bin/env python3

import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.timer import SessionTimer


class TestSessionTimer(unittest.TestCase):
    
    def setUp(self):
        self.timer = SessionTimer()
    
    def test_session_modes(self):
        """Test that session modes are properly defined"""
        expected_modes = {'short': 5, 'medium': 15, 'long': 25}
        self.assertEqual(self.timer.SESSION_MODES, expected_modes)
    
    def test_invalid_mode(self):
        """Test handling of invalid session mode"""
        result = self.timer.start_session('invalid')
        self.assertFalse(result)
    
    def test_custom_session_invalid_duration(self):
        """Test custom session with invalid duration"""
        result = self.timer.start_custom_session(0)
        self.assertFalse(result)
        
        result = self.timer.start_custom_session(-5)
        self.assertFalse(result)
    
    def test_list_modes(self):
        """Test list_modes method runs without error"""
        # This test just ensures the method can be called
        try:
            self.timer.list_modes()
        except Exception as e:
            self.fail(f"list_modes() raised an exception: {e}")


if __name__ == '__main__':
    unittest.main()