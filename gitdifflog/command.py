#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Allen
# @date  : 2025-03-10 09:21


"""
Implementation of git-difflog commands
"""

import datetime
import os
import re
import subprocess
import sys

from .config import get_config, setup_git_alias, edit_config


def get_project_name():
    """Get the current Git project name"""
    try:
        # Try to get remote URL
        remote_url = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url'],
                                             stderr=subprocess.PIPE,
                                             universal_newlines=True).strip()

        if remote_url:
            # Remove .git suffix if present
            if remote_url.endswith('.git'):
                remote_url = remote_url[:-4]

            # SSH URL format: git@github.com:username/repo.git
            ssh_match = re.match(r'git@.*:(.+)/([^/]+)$', remote_url)
            if ssh_match:
                return ssh_match.group(2)

            # HTTPS URL format: https://github.com/username/repo.git
            https_match = re.search(r'/([^/]+)/([^/]+)$', remote_url)
            if https_match:
                return https_match.group(2)
    except subprocess.CalledProcessError:
        pass

    # If no remote or parsing failed, use current directory name
    return os.path.basename(os.path.abspath(os.getcwd()))


def run_git_diff(args):
    """Run git diff and return the output"""
    cmd = ['git', 'diff'] + args
    try:
        return subprocess.check_output(cmd, stderr=subprocess.PIPE, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        if e.returncode != 0:
            print(f"Error running git diff: {e.stderr}")
            sys.exit(e.returncode)
        return ""


def cmd_init():
    """Initialize git-difflog by setting up git alias"""
    setup_git_alias()
    print("git-difflog has been initialized successfully.")


def cmd_config():
    """Edit the configuration file"""
    edit_config()


def cmd_diff(args):
    """Run git diff and save the output"""
    # Get config
    config = get_config()
    difflog_config = config['difflog']

    # Get output directory
    output_dir = difflog_config['outputdir']

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get project name
    project_name = get_project_name()

    # Get current timestamp
    timestamp = datetime.datetime.now().strftime(difflog_config['timestamp_format'])

    # Format output filename
    filename = difflog_config['filename_format'].format(
        project=project_name,
        timestamp=timestamp
    )
    output_path = os.path.join(output_dir, filename)

    # Run git diff and get output
    diff_output = run_git_diff(args)

    # If there's diff output, save to file
    if diff_output.strip():
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(diff_output)
        print(f"Diff saved to: {output_path}")
    else:
        print("No diff output to save.")

    # Print diff output to console if configured
    if difflog_config['show_diff']:
        print(diff_output)
