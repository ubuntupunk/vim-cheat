# Vim Cheat Sheet | rofi / fzf launcher

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/ubuntupunk/vim-prompt/blob/main/src/vim_prompt/readme/Dark-Cover.png">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/ubuntupunk/vim-prompt/blob/main/src/vim_prompt/readme/Light-Cover.png">
  <img alt="Vim Prompt Cover" src="https://github.com/ubuntupunk/vim-prompt/blob/main/src/vim_prompt/readme/Light-Cover.png">
</picture>

This project provides two helpers to access to **Vim commands** and **shortcuts** via an **interactive cheat sheet**. Using the helpers may assist those wanting to learn more about Vim. This version is for posix-compliant systems that are able to install fzf/rofi, if you want the Windows version use [FlowLauncher Plugin VimCheatSheet](https://github.com/MoAlSeifi/Flow.Launcher.Plugin.VimCheatSheet)

## Versions

There are two versions to suit different user preferences:

1. **CLI Version**: Ideal for users who prefer interacting through the command line.
2. **Rofi Popup Version**: Designed for users who prefer a graphical interface, providing a visually appealing and intuitive experience, great for tiling window managers like [i3](https://i3wm.org/) and [bspwm](https://github.com/baskerville/bspwm).

## Usage

| Keyword        | Description                                                                    | Example     |
| -------------- | ------------------------------------------------------------------------------ | ----------- |
| `fzf-vim` | Search for vim**commands** and **shortcuts** for a given `query` | enter to open Vim Cheat Sheet |
| `rofi-vim` | Search for vim**commands** and **shortcuts** for a given `query` | enter to open Vim Cheat Sheet |

## Features

* Search for Vim Commands either by their description or their Hotkey.
* Hitting enter on a command will redirect to [Vim Cheat Sheet](https://vim.rtorr.com/ "rtorr website") on the same command.

* Command fragments have not been tested and my not be fully functional, please report if any of them didn't work.

## Installation

### Manual Installation

* Download the [Latest Release](https://github.com/ubuntpunk/rofi-vim/releases/latest)
* Extract the archive and copy the files to `~/.local/share/rofi-vim`

### System requirements
- Rofi
- Fzf

### Installation

```python
pip install vim-prompt
```
### Install Helpers for Ubuntu/Debian

```bash
sudo apt install rofi fzf
```

### Operation
`fzf-vim`  `# Uses fzf interface`

`rofi-vim`  `# Uses rofi interface`

## Disclaimer

* The database of this repository is the result of the work of [Vim Cheat Sheet](https://vim.rtorr.com/ "rtorr website")
and based upon the [FlowLauncher Plugin VimCheatSheet Project](https://github.com/MoAlSeifi/Flow.Launcher.Plugin.VimCheatSheet)

* This project is not associated with Vim Cheat Sheet or FlowLauncher.

## References

- Powered by [Vim Cheat Sheet](https://vim.rtorr.com/ "rtorr website") as source for [commands.json](https://github.com/ubuntpunk/rofi-vim/blob/main/db/commands.json "commands json database")
