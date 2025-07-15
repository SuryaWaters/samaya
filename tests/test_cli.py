#!/usr/bin/env python3

import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.cli import create_parser


class TestCLI(unittest.TestCase):
    
    def setUp(self):
        self.parser = create_parser()
    
    def test_parser_creation(self):
        """Test that parser is created successfully"""
        self.assertIsNotNone(self.parser)
        self.assertEqual(self.parser.prog, 'samaya')
    
    def test_valid_modes(self):
        """Test parsing of valid session modes"""
        args = self.parser.parse_args(['short'])
        self.assertEqual(args.mode, 'short')
        
        args = self.parser.parse_args(['medium'])
        self.assertEqual(args.mode, 'medium')
        
        args = self.parser.parse_args(['long'])
        self.assertEqual(args.mode, 'long')
    
    def test_custom_time_argument(self):
        """Test parsing of custom time argument"""
        args = self.parser.parse_args(['--time', '10'])
        self.assertEqual(args.time, 10)
        
        args = self.parser.parse_args(['-t', '30'])
        self.assertEqual(args.time, 30)
    
    def test_list_modes_flag(self):
        """Test list modes flag"""
        args = self.parser.parse_args(['--list-modes'])
        self.assertTrue(args.list_modes)
    
    def test_no_arguments(self):
        """Test parsing with no arguments"""
        args = self.parser.parse_args([])
        self.assertIsNone(args.mode)
        self.assertIsNone(args.time)
        self.assertFalse(args.list_modes)


if __name__ == '__main__':
    unittest.main()