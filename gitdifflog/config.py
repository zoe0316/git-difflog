#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Allen
# @date  : 2025-03-10 09:21
"""
Configuration management for git-difflog
"""

import configparser
import os
import subprocess

DEFAULT_CONFIG = """[difflog]
# Output directory for saved diffs
outputdir = ~/git-difflog-output

# Format for the diff filename (available variables: {project}, {timestamp})
filename_format = {project}-{timestamp}.diff

# Timestamp format (using Python's datetime format strings)
timestamp_format = %Y-%m-%d_%H%M%S

# Whether to automatically display the diff in terminal
show_diff = true
"""


def get_config_file_path():
    """Return the path to the config file"""
    return os.path.expanduser("~/.git-difflog.conf")


def ensure_config_exists():
    """Make sure the config file exists, create with defaults if it doesn't"""
    config_path = get_config_file_path()

    if not os.path.exists(config_path):
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(DEFAULT_CONFIG)
        print(f"Created default configuration at {config_path}")

    return config_path


def get_config():
    """Get the configuration"""
    ensure_config_exists()
    config_path = get_config_file_path()

    # 禁用插值功能，这样 % 符号不会被当作变量
    config = configparser.ConfigParser(interpolation=None)
    config.read(config_path)

    # Ensure required sections and values exist
    if 'difflog' not in config:
        config['difflog'] = {}

    difflog_config = config['difflog']

    # Set defaults for missing values (as strings)
    if 'outputdir' not in difflog_config:
        difflog_config['outputdir'] = "~/git-difflog-output"
    if 'filename_format' not in difflog_config:
        difflog_config['filename_format'] = "{project}-{timestamp}.diff"
    if 'timestamp_format' not in difflog_config:
        difflog_config['timestamp_format'] = "%Y-%m-%d_%H%M%S"
    if 'show_diff' not in difflog_config:
        difflog_config['show_diff'] = "true"

    # Create a processed config dictionary
    processed_config = {
        'difflog': {
            # Expand user paths
            'outputdir': os.path.expanduser(difflog_config['outputdir']),
            'filename_format': difflog_config['filename_format'],
            'timestamp_format': difflog_config['timestamp_format'],
            # Convert string to boolean
            'show_diff': difflog_config['show_diff'].lower() in ('true', 'yes', 't', 'y', '1')
        }
    }

    return processed_config


def setup_git_alias():
    """Set up git alias for difflog"""
    try:
        # Check if alias already exists
        output = subprocess.check_output(['git', 'config', '--global', '--get', 'alias.difflog'],
                                         stderr=subprocess.PIPE,
                                         universal_newlines=True)
        print("git difflog alias already exists.")
    except subprocess.CalledProcessError:
        # Set the alias
        subprocess.run(['git', 'config', '--global', 'alias.difflog', '!git-difflog'],
                       check=True)
        print("git difflog alias has been set up successfully.")


def edit_config():
    """Open the config file in the default editor"""
    config_path = ensure_config_exists()

    if os.name == 'posix':  # macOS, Linux, etc.
        editor = os.environ.get('EDITOR', 'nano')
    else:  # Windows
        editor = 'notepad'

    try:
        subprocess.run([editor, config_path], check=True)
        print(f"Configuration file opened with {editor}.")
    except subprocess.CalledProcessError as e:
        print(f"Error opening config file: {e}")
