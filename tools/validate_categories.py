import json
import re
from pathlib import Path
from typing import Dict, Set, List
from collections import defaultdict

# Get package root directory
PACKAGE_ROOT = Path(__file__).parent.parent
SRC_PATH = PACKAGE_ROOT / "src" / "vim_prompt"
DB_PATH = SRC_PATH / "db"

def load_json(file_path: Path) -> dict:
    """Load and parse JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def validate_categories():
    """Validate category assignments and pattern matching."""
    # Load data
    categories_data = load_json(DB_PATH / "categories.json")
    mappings_data = load_json(DB_PATH / "command_mappings.json")
    
    categories = categories_data["categories"]
    commands = mappings_data["command_mappings"]
    
    # Track validation results
    errors = []
    warnings = []
    stats = defaultdict(int)
    category_usage = defaultdict(list)
    
    # Validate each command
    for cmd_key, cmd_data in commands.items():
        current_category = cmd_data["category"]
        description = cmd_data["canonical_description"].lower()
        
        # Track category usage
        category_usage[current_category].append(cmd_key)
        stats["total_commands"] += 1
        
        # Check if category exists
        if current_category not in categories:
            errors.append(f"Invalid category '{current_category}' for command '{cmd_key}'")
            continue
        
        # Check if any pattern matches
        matched_categories = set()
        for cat_name, cat_data in categories.items():
            for pattern in cat_data["patterns"]:
                if (re.search(pattern, cmd_key, re.IGNORECASE) or 
                    re.search(pattern, description, re.IGNORECASE)):
                    matched_categories.add(cat_name)
        
        # Validate categorization
        if not matched_categories:
            warnings.append(f"Command '{cmd_key}' doesn't match any patterns for its category '{current_category}'")
        elif current_category not in matched_categories:
            other_cats = matched_categories - {current_category}
            if other_cats:
                warnings.append(f"Command '{cmd_key}' might be better categorized as: {', '.join(other_cats)}")
        
        stats["properly_categorized"] += 1 if current_category in matched_categories else 0
    
    # Print validation results
    print("\n=== Category Validation Report ===\n")
    
    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"❌ {error}")
    
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"⚠️  {warning}")
    
    print("\nCategory Usage:")
    for category in sorted(categories.keys()):
        cmd_count = len(category_usage[category])
        print(f"• {categories[category]['name']}: {cmd_count} commands")
        if cmd_count == 0:
            warnings.append(f"Category '{category}' is not used by any commands")
    
    print("\nStatistics:")
    print(f"Total commands: {stats['total_commands']}")
    print(f"Properly categorized: {stats['properly_categorized']}")
    print(f"Categorization rate: {(stats['properly_categorized'] / stats['total_commands'] * 100):.1f}%")
    
    return len(errors) == 0

if __name__ == "__main__":
    success = validate_categories()
    exit(0 if success else 1)