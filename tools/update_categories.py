import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
from colorama import Fore, Style, init
from collections import defaultdict

# Initialize colorama
init(autoreset=True)

# Get package root directory
PACKAGE_ROOT = Path(__file__).parent.parent
SRC_PATH = PACKAGE_ROOT / "src" / "vim_prompt"
DB_PATH = SRC_PATH / "db"

class Colors:
    ERROR = Fore.RED
    WARNING = Fore.YELLOW
    SUCCESS = Fore.GREEN
    INFO = Fore.CYAN
    BOLD = Style.BRIGHT
    RESET = Style.RESET_ALL

def print_header(text: str):
    print(f"\n{Colors.BOLD}{Colors.INFO}=== {text} ==={Colors.RESET}\n")

def print_error(text: str):
    print(f"{Colors.ERROR}❌ {text}{Colors.RESET}")

def print_warning(text: str):
    print(f"{Colors.WARNING}⚠️  {text}{Colors.RESET}")

def print_success(text: str):
    print(f"{Colors.SUCCESS}✓ {text}{Colors.RESET}")

def load_json(file_path: Path) -> dict:
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(data: dict, file_path: Path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def get_all_patterns(category_data: dict) -> List[Tuple[str, str, str]]:
    patterns = []
    cat_name = category_data["name"]
    
    if "patterns" in category_data:
        patterns.extend([(p, cat_name, "") for p in category_data["patterns"]])
    
    if "subcategories" in category_data:
        for subcat_key, subcat_data in category_data["subcategories"].items():
            patterns.extend([(p, cat_name, subcat_key) for p in subcat_data["patterns"]])
    
    return patterns

def get_available_categories(categories: Dict) -> List[str]:
    available = []
    for cat_key, cat_data in categories.items():
        available.append(cat_key)
        if "subcategories" in cat_data:
            available.extend(subcat_key for subcat_key in cat_data["subcategories"].keys())
    return sorted(available)

def resolve_categorization(cmd_key: str, current_cat: str, suggested_cats: List[str], 
                         description: str, available_cats: List[str]) -> str:
    print(f"\n{Colors.BOLD}Command:{Colors.RESET} {cmd_key}")
    print(f"{Colors.BOLD}Description:{Colors.RESET} {description}")
    print(f"{Colors.BOLD}Current category:{Colors.RESET} {current_cat}")
    print(f"{Colors.BOLD}Suggested categories:{Colors.RESET} {', '.join(suggested_cats) if suggested_cats else 'None'}")
    
    while True:
        print("\nOptions:")
        print("1. Keep current category")
        print("2. Choose from suggestions")
        print("3. Enter different category")
        print("4. Show all available categories")
        print("5. Skip this command")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            return current_cat
        elif choice == "2":
            if not suggested_cats:
                print_warning("No suggestions available")
                continue
                
            # Convert suggestions to list and sort for consistent numbering
            suggestions = sorted(list(suggested_cats))
            print("\nAvailable suggestions:")
            for i, cat in enumerate(suggestions, 1):
                print(f"{i}. {cat}")
            
            try:
                choice = input("\nChoose category number (or 'b' to go back): ").strip()
                if choice.lower() == 'b':
                    continue
                    
                idx = int(choice) - 1
                if 0 <= idx < len(suggestions):
                    return suggestions[idx]
                else:
                    print_error("Invalid selection number")
            except ValueError:
                print_error("Please enter a valid number or 'b' to go back")
        elif choice == "3":
            while True:
                print("\nAvailable categories:")
                for cat in available_cats:
                    print(f"• {cat}")
                new_cat = input("\nEnter category (or 'b' to go back): ").strip()
                
                if new_cat.lower() == 'b':
                    break
                if new_cat in available_cats:
                    return new_cat
                print_error("Invalid category")
        elif choice == "4":
            print("\nAvailable categories:")
            for cat in available_cats:
                print(f"• {cat}")
            input("\nPress Enter to continue...")
        elif choice == "5":
            return current_cat
        else:
            print_error("Invalid choice")

def update_categories():
    print_header("Starting Category Update")
    
    # Load data
    categories_data = load_json(DB_PATH / "categories.json")
    mappings_data = load_json(DB_PATH / "command_mappings.json")
    
    categories = categories_data["categories"]
    commands = mappings_data["command_mappings"]
    available_cats = get_available_categories(categories)
    
    # Track changes
    changes = []
    stats = {
        "total": 0,
        "changed": 0,
        "categories": defaultdict(int)  # Changed this line
    }
    
    # Process each command
    total_commands = len(commands)
    for idx, (cmd_key, cmd_data) in enumerate(commands.items(), 1):
        print(f"\r{Colors.INFO}Processing commands... {idx}/{total_commands}{Colors.RESET}", end="")
        
        current_category = cmd_data["category"]
        description = cmd_data["canonical_description"]
        
        # Find matching categories
        matched_categories = set()
        for cat_key, cat_data in categories.items():
            patterns = get_all_patterns(cat_data)
            for pattern, _, subcat_key in patterns:
                if (re.search(pattern, cmd_key, re.IGNORECASE) or 
                    re.search(pattern, description, re.IGNORECASE)):
                    matched_categories.add(subcat_key if subcat_key else cat_key)
        
        # Check if categorization needs review
        needs_review = (not matched_categories or 
                       current_category not in matched_categories)
        
        if needs_review:
            print()  # New line after progress
            new_category = resolve_categorization(
                cmd_key, current_category, list(matched_categories),
                description, available_cats
            )
            
            if new_category != current_category:
                changes.append(f"{cmd_key}: {current_category} -> {new_category}")
                commands[cmd_key]["category"] = new_category
                stats["changed"] += 1
        
        stats["total"] += 1
        stats["categories"][current_category] += 1  # Changed this line
    
    print()  # New line after progress
    
    # Save changes
    if changes:
        print_header("Changes Made")
        for change in changes:
            print(f"• {change}")
        
        save_json(mappings_data, DB_PATH / "command_mappings.json")
        print_success(f"\nUpdated {stats['changed']} of {stats['total']} commands")
        
        print_header("Category Distribution")
        for cat, count in sorted(stats["categories"].items()):
            percentage = (count / stats["total"]) * 100
            print(f"• {cat}: {count} commands ({percentage:.1f}%)")
    else:
        print_success("No changes needed")

if __name__ == "__main__":
    update_categories()