#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Allen
# @date  : 2025-03-10 09:21


"""
Main entry point for git-difflog
"""

import argparse
import sys

from .command import cmd_init, cmd_config, cmd_diff
from .config import ensure_config_exists


def main():
    """Main entry point"""
    # Ensure config file exists
    ensure_config_exists()

    # Create argument parser
    parser = argparse.ArgumentParser(
        description="Git extension to save diff outputs with timestamps."
    )

    # Add subcommands
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # init command
    init_parser = subparsers.add_parser('init', help='Initialize git-difflog')

    # config command
    config_parser = subparsers.add_parser('config', help='Edit configuration')

    # Parse known args to handle extra arguments for git diff
    args, extra_args = parser.parse_known_args()

    # If no command is specified, assume it's a diff command with all args
    if not args.command and len(sys.argv) > 1:
        cmd_diff(sys.argv[1:])
        return

    # Execute the command
    if args.command == 'init':
        cmd_init()
    elif args.command == 'config':
        cmd_config()
    else:
        # Default to diff with no args
        cmd_diff(extra_args)


if __name__ == "__main__":
    main()
