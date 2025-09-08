# Claude Code Settings Permission Format Fixer

A Python script that automatically fixes permission format issues in Claude Code's `settings.json` file by converting the old wildcard syntax (`command*`) to the new prefix matching syntax (`command:*`).

## Problem

When using Claude Code, you might encounter permission format warnings when running `claude doctor` (https://github.com/anthropics/claude-code/issues/7300):

```
permissions
    └ allow
      ├ "Bash(git status*)": Use ":*" for prefix matching, not just "*". Change to "Bash(git status:*)" for prefix matching.
      ├ "Bash(git log*)": Use ":*" for prefix matching, not just "*". Change to "Bash(git log:*)" for prefix matching.
      ├ "Bash(git diff*)": Use ":*" for prefix matching, not just "*". Change to "Bash(git diff:*)" for prefix matching.
```

This happens when Claude Code automatically generates permissions using the old format, but the newer version expects the updated syntax.

## Solution

This script automatically converts:
- `"Bash(git status*)"` → `"Bash(git status:*)"` 
- `"Bash(git log*)"` → `"Bash(git log:*)"` 
- `"Bash(npm run*)"` → `"Bash(npm run:*)"` 
- And any other similar patterns

## Installation

No installation required! Just download the script:

```bash
# Download the script
curl -O https://example.com/claude_settings_fixer.py
# or copy the script to your local machine
```

## Usage

### Basic Usage

```bash
python claude_settings_fixer.py <path_to_settings.json>
```

### Examples

```bash
# Current directory
python claude_settings_fixer.py settings.json

# User home directory (Linux/macOS)
python claude_settings_fixer.py ~/.claude/settings.json

# Windows
python claude_settings_fixer.py "C:\Users\YourName\AppData\Roaming\claude\settings.json"
```

### Dry Run (Preview Changes)

To see what changes would be made without applying them:

```bash
python claude_settings_fixer.py --dry-run ~/.claude/settings.json
```

### Finding Your Settings File

Common locations for Claude Code settings:

- **Linux/macOS**: `~/.claude/settings.json` or `~/.config/claude/settings.json`
- **Windows**: `%APPDATA%\claude\settings.json`
- **Current directory**: `./settings.json`

## Features

- ✅ **Safe**: Creates automatic backups before making changes
- ✅ **Smart**: Only fixes permissions that need updating
- ✅ **Preview**: Dry-run mode to see changes before applying
- ✅ **Validation**: Checks file exists and contains valid JSON
- ✅ **Clear feedback**: Shows exactly what will be changed
- ✅ **Error handling**: Helpful error messages for common issues

## Example Output

```
Claude Code Settings Permission Format Fixer
==================================================
Processing settings file: /Users/username/.claude/settings.json

Found 4 permission(s) to fix:
  • 'Bash(git status*)' -> 'Bash(git status:*)'
  • 'Bash(git log*)' -> 'Bash(git log:*)'
  • 'Bash(git diff*)' -> 'Bash(git diff:*)'
  • 'Bash(git show*)' -> 'Bash(git show:*)'

Created backup: /Users/username/.claude/settings.json.backup

Apply these changes to /Users/username/.claude/settings.json? (y/N): y

Settings updated successfully!
Original file backed up to: /Users/username/.claude/settings.json.backup

You can now run 'claude doctor' to verify the fixes.
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `settings_file` | Path to the Claude Code settings.json file (required) |
| `--dry-run` | Show what changes would be made without applying them |
| `--help` | Show help message and examples |

## Safety Features

- **Automatic backups**: Original file is backed up with `.backup` extension
- **Confirmation prompt**: Asks before applying changes (unless dry-run)
- **Validation**: Checks file exists and contains valid JSON before processing
- **Rollback**: If something goes wrong, restore from the `.backup` file

## Troubleshooting

### File Not Found
```
Error: File does not exist: /path/to/settings.json
```
**Solution**: Check the path to your settings file. Use `find` or `locate` to search for `settings.json`.

### Permission Denied
```
Error: Permission denied reading file: /path/to/settings.json
```
**Solution**: Run with appropriate permissions or change file ownership.

### Invalid JSON
```
Error: Invalid JSON in file /path/to/settings.json
```
**Solution**: The settings file is corrupted. Restore from a backup or recreate it.

### No Changes Needed
```
No permission format issues found. Settings are already up to date!
```
**Result**: Your settings are already using the correct format. No action needed.

## After Running the Script

1. Run `claude doctor` to verify the fixes
2. The warnings about permission format should be gone
3. Your original file is safely backed up as `settings.json.backup`

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## License

This script is provided as-is for fixing Claude Code permission format issues. Feel free to modify and distribute.
