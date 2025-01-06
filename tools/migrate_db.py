import json
from pathlib import Path
import re
from typing import Dict, List, Tuple

# Get package root directory
PACKAGE_ROOT = Path(__file__).parent.parent
SRC_PATH = PACKAGE_ROOT / "src" / "vim_prompt"
DB_PATH = SRC_PATH / "db"

def load_json(file_path: Path) -> dict:
    """Load and parse JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(data: dict, file_path: Path):
    """Save data as JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def get_all_patterns(category_data: dict) -> List[Tuple[str, str, str]]:
    """Recursively get all patterns from a category and its subcategories."""
    patterns = []
    cat_name = category_data["name"]
    
    # Add patterns from the main category
    if "patterns" in category_data:
        patterns.extend([(p, cat_name, "") for p in category_data["patterns"]])
    
    # Add patterns from subcategories
    if "subcategories" in category_data:
        for subcat_key, subcat_data in category_data["subcategories"].items():
            subcat_name = subcat_data["name"]
            patterns.extend([(p, cat_name, subcat_key) for p in subcat_data["patterns"]])
    
    return patterns

def categorize_command(cmd_key: str, description: str, categories: Dict) -> str:
    """Determine the best category for a command."""
    best_matches = []
    
    # Build pattern lookup with category and subcategory info
    for cat_key, cat_data in categories.items():
        patterns = get_all_patterns(cat_data)
        
        for pattern, cat_name, subcat_key in patterns:
            if (re.search(pattern, cmd_key, re.IGNORECASE) or 
                re.search(pattern, description, re.IGNORECASE)):
                if subcat_key:
                    best_matches.append(subcat_key)
                else:
                    best_matches.append(cat_key)
    
    # Return the most common category or 'uncategorized'
    if best_matches:
        from collections import Counter
        return Counter(best_matches).most_common(1)[0][0]
    return "uncategorized"

def migrate_db():
    """Migrate the command database to use new categories."""
    # Load data
    categories_data = load_json(DB_PATH / "categories.json")
    mappings_data = load_json(DB_PATH / "command_mappings.json")
    
    categories = categories_data["categories"]
    commands = mappings_data["command_mappings"]
    
    # Track changes
    changes = []
    stats = {"total": 0, "changed": 0, "categories": {}}
    
    # Process each command
    print("Starting migration...")
    for cmd_key, cmd_data in commands.items():
        stats["total"] += 1
        old_category = cmd_data["category"]
        description = cmd_data["canonical_description"]
        
        # Determine new category
        new_category = categorize_command(cmd_key, description, categories)
        
        # Track changes
        if old_category != new_category:
            changes.append(f"{cmd_key}: {old_category} -> {new_category}")
            stats["changed"] += 1
            commands[cmd_key]["category"] = new_category
        
        # Update stats
        stats["categories"][new_category] = stats["categories"].get(new_category, 0) + 1
    
    # Save changes
    if changes:
        print("\nChanges made:")
        for change in changes:
            print(f"• {change}")
        
        save_json(mappings_data, DB_PATH / "command_mappings.json")
        print(f"\nUpdated {stats['changed']} of {stats['total']} commands")
        
        print("\nCategory distribution:")
        for cat, count in sorted(stats["categories"].items()):
            percentage = (count / stats["total"]) * 100
            print(f"• {cat}: {count} commands ({percentage:.1f}%)")
    else:
        print("No changes needed")

if __name__ == "__main__":
    migrate_db()