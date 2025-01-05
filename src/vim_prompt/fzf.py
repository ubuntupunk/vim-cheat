#!/usr/bin/env python
#This is a cli fzf version of the rofi_vim script
#copyright (c) 2024 Ubuntpunk

import sys
import json
import subprocess
import webbrowser
import urllib.parse
import os



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
        #dprint(f"Number of commands being passed to fzf: {len(commands)}")  # Debug line
        process = subprocess.Popen(['fzf', '--height', '40%', '--layout=reverse', '--border'],
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   universal_newlines=True)
        
        output, _ = process.communicate('\n'.join(commands))
        return output.strip() if output else None
    # input_str = '\n'.join(commands).encode('utf-8')
    # result = subprocess.run(['fzf', '--height', '40%', '--layout=reverse', '--border'],
    #                         input=input_str,
    #                         capture_output=True,
    #                         text=False)
    # if result.stderr:
    #     print(f"fzf error: {result.stderr.decode('utf-8')}")
    #     return None
    # return result.stdout.decode('utf-8').strip()

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