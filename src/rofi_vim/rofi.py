#!/usr/bin/env python
#This is the rofi_vim launcher script

import sys
import os
import json
import subprocess
import webbrowser

def main():
    """Main function."""
    vim_commands = load_vim_commands('db/commands.json')
    formatted_commands = format_commands_for_rofi(vim_commands)
    selected_command_rofi = execute_rofi(formatted_commands)
    if selected_command_rofi:
        open_vim_command_url(selected_command_rofi)
    else:
        print("No command selected from rofi")

def load_vim_commands(file_path):
    """Load Vim commands from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

vim_commands = load_vim_commands('db/commands.json')
icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icon.png") #PLEASE FIX
print(f"Icon path: {icon_path}")  # Debug print
print(f"Icon exists: {os.path.exists(icon_path)}")  # Verify file exists

def format_commands_for_rofi(commands):
    """Format commands for rofi."""
    formatted_commands = []
    for command in commands:
        formatted_commands.append(f"{command['command']} | {command['name']} | {command['description']} | {command['rtorr_description']}")
    return formatted_commands

def execute_rofi(commands):
    """Execute rofi and return the selected command."""
    rofi_process = subprocess.Popen(
        # ['rofi', '-dmenu', '-i', '-show-icons', '-theme-str', 'entry { placeholder: ""; }', f'window {{ icon: "{icon_path}"; }}',
        #  '-theme-str', f'listview {{ columns: 1; }}', '-p','Vim Command:'],
        ['rofi','-dmenu', '-i', '-show-icons', '-theme-str', f'configuration {{ icon: "{icon_path}"; }}',
         '-theme-str', 'window { width: 35%; }','-theme-str', 'listview { columns: 1; }','-p', 'Vim Command:'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = rofi_process.communicate(input='\n'.join(commands))
    if stderr:
        print(f"rofi error: {stderr}")
        return None
    return stdout.strip()

def open_vim_command_url(selected_command):
    """Open the URL associated with the selected command."""
    if not selected_command:
        return
    parts = selected_command.split(" | ")
    if len(parts) != 4:
        print("Invalid command format")
        return
    rtorr_description = parts[3]
    url = f"https://vim.rtorr.com/#:~:text={rtorr_description}"
    webbrowser.open(url)

if __name__ == "__main__":
    formatted_commands = format_commands_for_rofi(vim_commands)
    selected_command_rofi = execute_rofi(formatted_commands)
    if selected_command_rofi:
        open_vim_command_url(selected_command_rofi)
    else:
        print("No command selected from rofi")

if __name__ == "__main__":
    main()