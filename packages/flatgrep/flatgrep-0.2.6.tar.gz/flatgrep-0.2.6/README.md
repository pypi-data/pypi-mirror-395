# Flatgrep ⚡*v0.2.6*
> Automated search for boring CLI.

Tired of typing by hand `flatpak list | grep com.something.veryobnoxious`?  
Try **Flatgrep** for fuzzy search and grep what you want in just seconds. 

* **Fast and easy install apps from Flathub:**
```bash
flatgrep install mpv
```

* **Quickly copy app id from installed apps:**
```bash
flatgrep copy mpv
```

* **Swiftly uninstall flatpak app by regular name:**
```bash
flatgrep remove vlc
```

* **Fuzzy search all app ids from installed apps:**
```bash
flatgrep list
```

* **Copy id if installed, otherwise install from flathub:**
```bash
flatgrep mpv
```

# Installation
* **Quick Installation:** 
```bash
pipx install flatgrep
```

## What is Flatgrep?

**Flatgrep** is a smart, fuzzy-finding command-line wrapper for Flatpak that makes searching, installing, and managing your applications a breeze. It enhances the standard `flatpak` commands with an interactive `fzf` interface, ensuring you find and select the right application quickly, even with typos or partial names.

## Why Flatgrep?

Tired of trying to guess the exact application ID for a Flatpak? The default `flatpak search` can be cumbersome. Flatgrep solves this by providing a powerful and intuitive search layer on top of Flatpak.

* **Typo-proof Searching**: Can't remember if it's `Discord` or `discord`? Just type `disc` and let the fuzzy finder show you the options.
* **Interactive Selection**: No more manually copying and pasting long app IDs like `org.gimp.GIMP`. Just search, select from the list, and let Flatgrep handle the rest. The selected ID is copied to your clipboard automatically.
* **Unified Workflow**: Use one consistent and powerful search tool to find, install, run, and uninstall your Flatpak apps.

## Features

* ✅ **Smart Interactive Search**: Uses `fzf` to provide a fuzzy search interface for both locally installed apps and the entire Flathub repository.
* 🧠 **Intelligent Filtering**:
    * If there's one perfect match, it's selected automatically.
    * If there are multiple matches, you can choose from an interactive list using `fzf`.
    * If no initial match is found, it falls back to a fuzzy search over the entire list of apps.
* 📋 **Clipboard Integration**: The selected application ID is automatically copied to your clipboard for convenience.
* 🎨 **Rich Terminal Output**: Utilizes the `rich` library for clean, modern, and colorful command-line feedback.
* 🚀 **Full Management Suite**: Provides intuitive commands for `search`, `install`, `run`, and `uninstall`.

## Command Table 
**Usage:** `flatgrep [install|search|remove|run|copy|list] app name`
| Action                          | Linux Command                          |
|---------------------------------|----------------------------------------|
| **Install an app from Flathub** | `flatgrep install app name`            |
| **Fuzzy search installed apps** | `flatgrep list`                        |
| **Copy installed app id**       | `flatgrep copy app name`               |
| **Run an app**                  | `flatgrep run app name`                |
| **Uninstall an app**            | `flatgrep uninstall app name`          |
| **Uninstall an app**            | `flatgrep remove app name`             |
| **Copy local / install**        | `flatgrep app name`                    |

**Examples:**
| Action                          | Example Command                | Description |
|---------------------------------|--------------------------------|-------------|
| **Install an app from Flathub** | `flatgrep install vlc`         | Installs the VLC media player via Flathub. |
| **Fuzzy search installed apps** | `flatgrep list`                | Lists all installed applications. |
| **Copy installed app id**       | `flatgrep copy gimp`           | Copies the installed GIMP app ID to the clipboard. |
| **Run an app**                  | `flatgrep run vlc`             | Runs the VLC media player. |
| **Uninstall an app**            | `flatgrep remove vlc`          | Removes/uninstalls VLC. |
| **Copy local / install**        | `flatgrep gimp`                | Searches for the app and allows copying or installing it. |


---

## Building Instructions 

#### Prerequisites

Before you begin, make sure you have the following installed on your system:
* [Python 3.8+](https://www.python.org/downloads/)
* [Flatpak](https://flatpak.org/setup/)
* [fzf](https://github.com/junegunn/fzf?tab=readme-ov-file#installation)
* [uv python package manager](https://docs.astral.sh/uv/getting-started/installation/)
* [pipx (optional)](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx)

You can install `uv` using pipx:
```bash
pipx install uv
```

You can install `fzf` using your system's package manager:
```bash
# Debian/Ubuntu
sudo apt install fzf

# Fedora
sudo dnf install fzf

# Arch Linux
sudo pacman -S fzf
```

#### Clone Git Repository
```bash
git clone https://github.com/rodhfr/flatgrep.git
cd flatgrep
```

#### Setup environment with uv
```bash
uv install
```

#### Test
```bash
uv run flatgrep
```

---

## Management

### Released Features ✅
- [x] Search installed Flatpak app IDs.
- [x] Copy app IDs to the clipboard.
- [x] Install Flatpaks via fuzzy search with `--flathub` flag.
- [x] Rich-text console.
- [x] Run Flatpaks with `run` mode 'feature: 2025-09-15.v0.1.1'
- [x] Write building instructions and program description. 'feature: 2025-09-16.v0.1.3'

### Planned 🛠️
- [x] Write installation guide.
- [x] Release in some package manager.
- [x] Write documentation.
- [x] Run mode update: Auto install app if not available.
- [x] Proper sanitize search command.
- [ ] Search mode also searches by app names not only app ids.

### Potential Features 🤔
- [ ] Other package managers like dnf/pacman/aur helpers.
