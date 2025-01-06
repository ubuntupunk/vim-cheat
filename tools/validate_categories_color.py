import json
import re
from pathlib import Path
from typing import Dict, Set, List
from collections import defaultdict
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Get package root directory
PACKAGE_ROOT = Path(__file__).parent.parent
SRC_PATH = PACKAGE_ROOT / "src" / "vim_prompt"
DB_PATH = SRC_PATH / "db"

class Colors:
    """Color constants for output formatting."""
    ERROR = Fore.RED
    WARNING = Fore.YELLOW
    SUCCESS = Fore.GREEN
    INFO = Fore.CYAN
    BOLD = Style.BRIGHT
    RESET = Style.RESET_ALL

def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{Colors.BOLD}{Colors.INFO}=== {text} ==={Colors.RESET}\n")

def print_error(text: str):
    """Print an error message."""
    print(f"{Colors.ERROR}❌ {text}{Colors.RESET}")

def print_warning(text: str):
    """Print a warning message."""
    print(f"{Colors.WARNING}⚠️  {text}{Colors.RESET}")

def print_success(text: str):
    """Print a success message."""
    print(f"{Colors.SUCCESS}✓ {text}{Colors.RESET}")

def print_category_stat(name: str, count: int, total: int):
    """Print category statistics with color based on usage."""
    percentage = (count / total * 100) if total > 0 else 0
    if percentage == 0:
        color = Colors.ERROR
    elif percentage < 5:
        color = Colors.WARNING
    else:
        color = Colors.SUCCESS
    print(f"{color}• {name}: {count} commands ({percentage:.1f}%){Colors.RESET}")

def load_json(file_path: Path) -> dict:
    """Load and parse JSON file with detailed error reporting."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print_error(f"Invalid JSON in {file_path}")
        print_error(f"Error at line {e.lineno}, column {e.colno}: {e.msg}")
        with open(file_path, 'r') as f:
            lines = f.readlines()
            if e.lineno <= len(lines):
                print(f"{Colors.WARNING}Line {e.lineno}:{Colors.RESET} {lines[e.lineno-1].rstrip()}")
                print(f"{' ' * (e.colno + 7)}{Colors.ERROR}^{Colors.RESET}")
        raise
    except FileNotFoundError:
        print_error(f"File not found: {file_path}")
        raise

def get_all_patterns(category_data: dict) -> List[tuple[str, str]]:
    """Recursively get all patterns from a category and its subcategories."""
    patterns = []
    
    # Add patterns from the main category
    if "patterns" in category_data:
        patterns.extend([(p, category_data["name"]) for p in category_data["patterns"]])
    
    # Add patterns from subcategories
    if "subcategories" in category_data:
        for subcat_name, subcat_data in category_data["subcategories"].items():
            patterns.extend([(p, f"{category_data['name']} - {subcat_data['name']}")
                           for p in subcat_data["patterns"]])
    
    return patterns

def validate_categories():
    """Validate category assignments and pattern matching."""
    print_header("Starting Category Validation")
    
    # Load data
    try:
        categories_data = load_json(DB_PATH / "categories.json")
        mappings_data = load_json(DB_PATH / "command_mappings.json")
    except (json.JSONDecodeError, FileNotFoundError):
        return False
    
    categories = categories_data["categories"]
    commands = mappings_data["command_mappings"]
    
    # Track validation results
    errors = []
    warnings = []
    stats = defaultdict(int)
    category_usage = defaultdict(list)
    
    # Build pattern lookup
    all_patterns = []
    for cat_name, cat_data in categories.items():
        all_patterns.extend(get_all_patterns(cat_data))
    
    # Validate each command
    total_commands = len(commands)
    for idx, (cmd_key, cmd_data) in enumerate(commands.items(), 1):
        # Show progress
        print(f"\r{Colors.INFO}Processing commands... {idx}/{total_commands}{Colors.RESET}", end="")
        
        current_category = cmd_data["category"]
        description = cmd_data["canonical_description"].lower()
        
        # Track category usage
        category_usage[current_category].append(cmd_key)
        stats["total_commands"] += 1
        
        # Check if category exists
        category_found = False
        for cat_name, cat_data in categories.items():
            if cat_name == current_category:
                category_found = True
                break
            if "subcategories" in cat_data:
                if current_category in cat_data["subcategories"]:
                    category_found = True
                    break
        
        if not category_found:
            errors.append(f"Invalid category '{current_category}' for command '{cmd_key}'")
            continue
        
        # Check if any pattern matches
        matched_categories = set()
        for pattern, cat_name in all_patterns:
            if (re.search(pattern, cmd_key, re.IGNORECASE) or 
                re.search(pattern, description, re.IGNORECASE)):
                matched_categories.add(cat_name)
        
        # Validate categorization
        if not matched_categories:
            warnings.append(f"Command '{cmd_key}' doesn't match any patterns")
        elif current_category not in [cat.split(" - ")[0] for cat in matched_categories]:
            warnings.append(f"Command '{cmd_key}' might be better categorized as: {', '.join(matched_categories)}")
        
        stats["properly_categorized"] += 1 if matched_categories else 0
    
    print()  # New line after progress
    
    # Print validation results
    if errors:
        print_header("Errors")
        for error in errors:
            print_error(error)
    
    if warnings:
        print_header("Warnings")
        for warning in warnings:
            print_warning(warning)
    
    print_header("Category Usage")
    for category in sorted(categories.keys()):
        cmd_count = len(category_usage[category])
        print_category_stat(categories[category]["name"], cmd_count, stats["total_commands"])
        if cmd_count == 0:
            warnings.append(f"Category '{category}' is not used by any commands")
    
    print_header("Statistics")
    total = stats["total_commands"]
    properly_categorized = stats["properly_categorized"]
    categorization_rate = (properly_categorized / total * 100) if total > 0 else 0
    
    print(f"{Colors.BOLD}Total commands:{Colors.RESET} {total}")
    print(f"{Colors.BOLD}Properly categorized:{Colors.RESET} {properly_categorized}")
    if categorization_rate >= 90:
        print_success(f"Categorization rate: {categorization_rate:.1f}%")
    elif categorization_rate >= 75:
        print_warning(f"Categorization rate: {categorization_rate:.1f}%")
    else:
        print_error(f"Categorization rate: {categorization_rate:.1f}%")
    
    return len(errors) == 0

if __name__ == "__main__":
    success = validate_categories()
    exit(0 if success else 1)