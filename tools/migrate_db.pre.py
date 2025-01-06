#!/usr/bin/env python

# This script migrates the old commands.json to the new database structure.

import json
import os
from pathlib import Path
import re
from typing import Dict, Optional

# Get package root directory
PACKAGE_ROOT = Path(__file__).parent.parent

SRC_PATH = PACKAGE_ROOT / "src" / "vim_prompt"
DB_PATH = SRC_PATH / "db"

def load_categories() -> Dict:
    """Load category definitions."""
    with open(DB_PATH / "categories.json") as f:
        return json.load(f)["categories"]

def categorize_command(command: str, description: str, categories: Dict) -> str:
    """
    Categorize command based on patterns in command or description.
    Returns category id or 'uncategorized'.
    """
    command = command.lower()
    description = description.lower()
    
    for category_id, category in categories.items():
        patterns = category["patterns"]
        
        # Check if command or description matches any pattern
        for pattern in patterns:
            if (re.search(pattern, command) or 
                re.search(pattern, description)):
                return category_id
    
    return "uncategorized"

def migrate_db():
    """Migrate old commands.json to new database structure."""
    # Load categories
    categories = load_categories()
# Update paths to use package structure
    old_commands_path = DB_PATH / "commands.json"
    new_rtorr_path = DB_PATH / "rtorr_commands.json"
    new_mappings_path = DB_PATH / "command_mappings.json"

    # Load existing commands
    with open(old_commands_path, 'r') as f:
        old_commands = json.load(f)

    # Create rtorr_commands.json
    rtorr_data = {
        "source": "rtorr",
        "url": "https://vim.rtorr.com/",
        "commands": {}
    }

    # Create command_mappings.json
    mappings_data = {
        "command_mappings": {}
    }

    # Migrate each command
    for command in old_commands:
        cmd_key = command["command"]
        description = command["description"]

        # Add to rtorr commands
        rtorr_data["commands"][cmd_key] = {
            "fragment": description,
            "available": True
        }

 # Categorize based on patterns
        category = categorize_command(cmd_key, description, categories)

        # Add to mappings
        mappings_data["command_mappings"][cmd_key] = {
            "canonical_description": description,
            "aliases": [description],
            "category": category
        }

    # Create db directory if it doesn't exist
    Path('db').mkdir(exist_ok=True)

    # Save new files
    with open(new_rtorr_path, 'w') as f:
        json.dump(rtorr_data, f, indent=2)

    with open(new_mappings_path, 'w') as f:
        json.dump(mappings_data, f, indent=2)

    print("Migration complete!")
    print(f"You can now safely remove {old_commands_path}")

if __name__ == "__main__":
    migrate_db()