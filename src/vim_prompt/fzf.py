#!/usr/bin/env python
#This is a cli fzf version of the rofi_vim script
#copyright (c) 2024 Ubuntpunk

import sys
import json
import subprocess
import webbrowser
import urllib.parse
import os

RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

def check_fzf_installed():
    """Check if fzf is available in the system."""
    try:
        subprocess.run(['which', 'fzf'], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def get_package_manager_instructions():
    """Return installation instructions for various package managers."""
    instructions = f"""
    {RED}{BOLD}FZF is not installed. Please install it using one of the following methods:

    {BLUE}For Debian/Ubuntu:{RESET}
    sudo apt update && sudo apt install fzf

    {BLUE}For Arch Linux:{RESET}
    sudo pacman -S fzf

    {BLUE}For Fedora:{RESET}
    sudo dnf install fzf

    {BLUE}For macOS:{RESET}
    brew install fzf

    {GREEN}Alternative methods:{RESET}
    1. Using Git:
    git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
    ~/.fzf/install

    2. Using Python pip:
    pip install fzf

    {RED}{BOLD}Please install fzf and try again.{RESET}
"""
    return instructions

def load_vim_commands(file_path):
    """Load Vim commands from a JSON file."""
    package_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(package_dir, 'db', 'commands.json')     
    with open(full_path, 'r') as file:
        return json.load(file)

def format_commands_for_fzf(commands):
    """Format commands for fzf."""
    formatted_commands = []
    for command in commands:
        formatted_commands.append(f"{command['command']} | {command['name']} | {urllib.parse.unquote(command['description'])} | {urllib.parse.unquote(command['rtorr_description'])}")
    return formatted_commands

def execute_fzf(commands):
    """Execute fzf and return the selected command."""
    if not check_fzf_installed():
        print(get_package_manager_instructions())
        sys.exit(1)
    process = subprocess.Popen(['fzf', '--height', '40%', '--layout=reverse', '--border'],
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   universal_newlines=True)
        
    output, _ = process.communicate('\n'.join(commands))
    return output.strip() if output else None
 
def open_vim_command_url(selected_command):
    """Open the URL associated with the selected command."""
    if not selected_command:
        return
    print(f"Processing selected command: {selected_command}")  # Debug print
    parts = selected_command.split(" | ")
    print(f"Split parts: {parts}")  # Debug print
    if len(parts) != 4:
        print("Invalid command format")
        return
    rtorr_description = parts[3]
    print(f"rtorr_description: {rtorr_description}")  # Debug print
    url = f"https://vim.rtorr.com/#:~:text={rtorr_description}"
    print(f"Opening URL: {url}")  # Debug print
    webbrowser.open(url)

def main():
    vim_commands = load_vim_commands('commands.json')
    formatted_commands = format_commands_for_fzf(vim_commands)
    selected_command_fzf = execute_fzf(formatted_commands)
    if selected_command_fzf:
        open_vim_command_url(selected_command_fzf)
    else:
        print("No command selected from fzf")

if __name__ == "__main__":
    main()