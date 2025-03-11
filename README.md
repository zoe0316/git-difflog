# git-difflog

A Git extension that runs `git diff` and saves the output to a configured directory with timestamps.

## Installation

Install using pip:

```bash
pip install git-difflog
```

Or clone the repository and install:

```bash
git clone https://github.com/zoe0316/git-difflog.git
cd git-difflog
python setup.py install
```

## Initialization

After installation, initialize git-difflog:

```bash
git difflog init
```

This will set up a Git alias so you can use `git difflog` as a command.

## Configuration

To edit the configuration file:

```bash
git difflog config
```

This will open the configuration file in your default editor. The configuration file is located at `~/.git-difflog.conf`.

Default configuration:

```ini
[difflog]
# Output directory for saved diffs
outputdir = ~/git-difflog-output

# Format for the diff filename (available variables: {project}, {timestamp})
filename_format = {project}-{timestamp}.diff

# Timestamp format (using Python's datetime format strings)
timestamp_format = %Y-%m-%d_%H%M%S

# Whether to automatically display the diff in terminal
show_diff = true
```

## Usage

Use `git difflog` just like you would use `git diff`:

```bash
# Show and save changes in working directory
git difflog

# Show and save staged changes
git difflog --staged

# Show and save changes between commits
git difflog HEAD~3 HEAD
```

The diff output will be saved to the configured directory with a filename based on your project name and current timestamp.

## License

MIT License
