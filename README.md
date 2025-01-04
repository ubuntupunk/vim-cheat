# Vim Cheat Sheet | rofi / fzf launcher

![dark-cover](https://github.com/ubuntupunk/vim-cheat/blob/main/src/rofi_vim/readme/Dark-Cover.png))
![light-cover](https://github.com/ubuntpunk/rofi-vim/blob/main/src/rofi_vim/readme/Light-Cover.png))

This project provides two helpers to access to **Vim commands** and **shortcuts** via an **interactive cheat sheet**


## Versions

There are two versions to suit different user preferences:

1. **CLI Version**: Ideal for users who prefer interacting through the command line.
2. **Rofi Popup Version**: Designed for users who prefer a graphical interface, providing a visually appealing and intuitive experience, great for tiling window managers like [i3](https://i3wm.org/) and [bspwm](https://github.com/baskerville/bspwm).

## Usage

| Keyword        | Description                                                                    | Example     |
| -------------- | ------------------------------------------------------------------------------ | ----------- |
| ``vm {query}`` | Search for vim**commands** and **shortcuts** for a given `query` | `vm exit` |

## Features

* Search for Vim Commands either by their description or their Hotkey.
* Hitting enter on a command will redirect to [Vim Cheat Sheet](https://vim.rtorr.com/ "rtorr website") on the same command.

* Command fragments have not been tested and my not be fully functional, please report if any of them didn't work.

## Installation

### Manual Installation

* Download the [Latest Release](https://github.com/ubuntpunk/rofi-vim/releases/latest)
* Extract the archive and copy the files to `~/.local/share/rofi-vim`


### Operation
`fzf-vim`  `# Uses fzf interface`

`rofi-vim`  `# Uses rofi interface`

## Disclaimer

* The database of this repository is the result of the work of [Vim Cheat Sheet](https://vim.rtorr.com/ "rtorr website")
and based upon the [FlowLauncher Plugin VimCheatSheet Project](https://github.com/MoAlSeifi/Flow.Launcher.Plugin.VimCheatSheet)

* This project is not associated with Vim Cheat Sheet or FlowLauncher.

## References

- Powered by [Vim Cheat Sheet](https://vim.rtorr.com/ "rtorr website") as source for [commands.json](https://github.com/ubuntpunk/rofi-vim/blob/main/db/commands.json "commands json database")
