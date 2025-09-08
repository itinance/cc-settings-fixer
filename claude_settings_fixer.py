#!/usr/bin/env python3
"""
Claude Code Settings Permission Format Fixer

This script fixes the permission format in Claude Code's settings.json file,
converting old wildcard syntax (command*) to new prefix syntax (command:*).

Usage: python fix_claude_settings.py <path_to_settings.json>
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Dict, Any, List


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Fix Claude Code permission format from 'command*' to 'command:*'",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python fix_claude_settings.py settings.json
  python fix_claude_settings.py ~/.claude/settings.json
  python fix_claude_settings.py "C:\\Users\\Me\\AppData\\Roaming\\claude\\settings.json"
        """
    )
    
    parser.add_argument(
        'settings_file',
        type=str,
        help='Path to the Claude Code settings.json file'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what changes would be made without applying them'
    )
    
    return parser.parse_args()


def validate_settings_file(file_path: Path) -> None:
    """Validate that the settings file exists and is readable."""
    if not file_path.exists():
        print(f"Error: File does not exist: {file_path}")
        sys.exit(1)
    
    if not file_path.is_file():
        print(f"Error: Path is not a file: {file_path}")
        sys.exit(1)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file {file_path}: {e}")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied reading file: {file_path}")
        sys.exit(1)


def fix_permission_format(permission: str) -> str:
    """
    Convert old permission format to new format.
    
    Examples:
    - "Bash(git status*)" -> "Bash(git status:*)"
    - "Bash(npm run*)" -> "Bash(npm run:*)"
    """
    # Pattern to match: Tool(command*) where * is at the end
    pattern = r'^(\w+\([^)]*?)(\*)(\))$'
    match = re.match(pattern, permission)
    
    if match:
        prefix = match.group(1)
        suffix = match.group(3)
        # Replace * with :*
        return f"{prefix}:*{suffix}"
    
    return permission


def process_permissions(data: Dict[str, Any]) -> tuple[Dict[str, Any], List[str]]:
    """Process the settings data and fix permission formats."""
    changes = []
    
    if "permissions" not in data:
        print("No permissions section found in settings.json")
        return data, changes
    
    permissions = data["permissions"]
    
    if "allow" in permissions:
        allow_list = permissions["allow"]
        if isinstance(allow_list, list):
            for i, permission in enumerate(allow_list):
                if isinstance(permission, str):
                    new_permission = fix_permission_format(permission)
                    if new_permission != permission:
                        allow_list[i] = new_permission
                        changes.append(f"'{permission}' -> '{new_permission}'")
    
    return data, changes


def backup_file(file_path: Path) -> Path:
    """Create a backup of the original file."""
    backup_path = file_path.with_suffix(f"{file_path.suffix}.backup")
    shutil.copy2(file_path, backup_path)
    return backup_path


def main():
    """Main function to fix Claude Code settings."""
    args = parse_arguments()
    
    print("Claude Code Settings Permission Format Fixer")
    print("=" * 50)
    
    try:
        # Validate settings file
        settings_path = Path(args.settings_file).resolve()
        validate_settings_file(settings_path)
        
        print(f"Processing settings file: {settings_path}")
        
        # Load and process settings
        with open(settings_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Fix permission formats
        updated_data, changes = process_permissions(data)
        
        if not changes:
            print("No permission format issues found. Settings are already up to date!")
            return
        
        print(f"\nFound {len(changes)} permission(s) to fix:")
        for change in changes:
            print(f"  • {change}")
        
        if args.dry_run:
            print("\n[DRY RUN] No changes were applied.")
            print("Remove --dry-run flag to apply these changes.")
            return
        
        # Create backup
        backup_path = backup_file(settings_path)
        print(f"\nCreated backup: {backup_path}")
        
        # Ask for confirmation
        response = input(f"\nApply these changes to {settings_path}? (y/N): ").strip().lower()
        
        if response in ['y', 'yes']:
            # Write updated settings
            with open(settings_path, 'w', encoding='utf-8') as f:
                json.dump(updated_data, f, indent=2)
            
            print(f"\nSettings updated successfully!")
            print(f"Original file backed up to: {backup_path}")
            print("\nYou can now run 'claude doctor' to verify the fixes.")
        else:
            print("Changes cancelled.")
            # Remove backup since no changes were applied
            backup_path.unlink()
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
