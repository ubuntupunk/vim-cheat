import json
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Tuple

def scrape_vimsheet() -> Dict:
    """Scrape commands from vimsheet.com."""
    url = "https://vimsheet.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    commands_data = {
        "source": "vimsheet",
        "url": url,
        "commands": {}
    }

    # Find all command sections
    sections = soup.find_all('div', class_='commands')
    
    for section in sections:
        # Find all command entries
        entries = section.find_all(['dt', 'dd'])
        
        # Process pairs of dt (command) and dd (description)
        for i in range(0, len(entries), 2):
            if i + 1 < len(entries):
                command = entries[i].get_text().strip()
                description = entries[i + 1].get_text().strip()
                
                # Skip empty or invalid commands
                if command and description:
                    commands_data["commands"][command] = {
                        "fragment": description,
                        "available": True
                    }

    return commands_data

def update_command_mappings(commands_data: Dict) -> Dict:
    """Update command_mappings.json with new commands."""
    try:
        with open('db/command_mappings.json', 'r') as f:
            mappings = json.load(f)
    except FileNotFoundError:
        mappings = {"command_mappings": {}}

    # Add new commands to mappings
    for command in commands_data["commands"]:
        if command not in mappings["command_mappings"]:
            description = commands_data["commands"][command]["fragment"]
            mappings["command_mappings"][command] = {
                "canonical_description": description,
                "aliases": [description],
                "category": "uncategorized"
            }

    return mappings

def main():
    # Scrape vimsheet.com
    print("Scraping vimsheet.com...")
    commands_data = scrape_vimsheet()
    
    # Save vimsheet commands
    print(f"Found {len(commands_data['commands'])} commands")
    with open('db/vimsheet_commands.json', 'w') as f:
        json.dump(commands_data, f, indent=2)
    print("Saved vimsheet_commands.json")

    # Update command mappings
    mappings = update_command_mappings(commands_data)
    with open('db/command_mappings.json', 'w') as f:
        json.dump(mappings, f, indent=2)
    print("Updated command_mappings.json")

if __name__ == "__main__":
    main()