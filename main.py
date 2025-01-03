import sys
import json
import subprocess
import webbrowser

def load_vim_commands(file_path):
    """Load Vim commands from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

vim_commands = load_vim_commands('db/commands.json')
icon_path = "assets/icon.png"

def format_commands_for_fzf(commands):
    """Format commands for fzf."""
    formatted_commands = []
    for command in commands:
        formatted_commands.append(f"{command['command']} | {command['name']} | {command['description']} | {command['rtorr_description']}")
    return formatted_commands

def execute_fzf(commands):
    """Execute fzf and return the selected command."""
    fzf_process = subprocess.Popen(
        ['fzf', '--height', '40%', '--layout=reverse', '--border'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = fzf_process.communicate(input='\n'.join(commands))
    if stderr:
        print(f"fzf error: {stderr}")
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
    formatted_commands = format_commands_for_fzf(vim_commands)
    selected_command_fzf = execute_fzf(formatted_commands)
    if selected_command_fzf:
        open_vim_command_url(selected_command_fzf)
    else:
        print("No command selected from fzf")

