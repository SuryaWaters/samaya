#!/usr/bin/env python3

import argparse
import sys
import os
from .timer import SessionTimer
from ._version import __version__


def create_parser():
    """Create and configure the argument parser"""
    parser = argparse.ArgumentParser(
        description='A minimal Pomodoro CLI timer for terminal environments with session tracking, ambient brown noise audio and session end bell. Completely local - no internet required, no data collection, full privacy.',
        prog='samaya'
    )
    
    parser.add_argument(
        'mode',
        choices=['short', 'medium', 'long', 'stats'],
        nargs='?',
        help='Session mode: short (5 min), medium (15 min), long (25 min), stats (display session statistics and usage history)'
    )
    
    parser.add_argument(
        '--time', '-t',
        type=int,
        help='Custom session duration in minutes'
    )
    
    parser.add_argument(
        '--list-modes',
        action='store_true',
        help='List available session modes and exit'
    )
    
    parser.add_argument(
        '--clear',
        action='store_true',
        help='Clear all session statistics (use with stats mode)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    return parser


def main():
    """Main CLI entry point"""
    # Set terminal title
    sys.stdout.write("\033]0;samaya - a pomodoro cli\007")
    sys.stdout.flush()
    
    parser = create_parser()
    args = parser.parse_args()
    
    timer = SessionTimer()
    
    if args.list_modes:
        timer.list_modes()
        return
    
    if args.mode == 'stats':
        if args.clear:
            timer.stats.clear_stats()
        else:
            timer.stats.display_stats()
        return
    
    if not args.mode and not args.time:
        parser.print_help()
        sys.exit(1)
    
    if args.time:
        success = timer.start_custom_session(args.time)
    else:
        success = timer.start_session(args.mode)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()