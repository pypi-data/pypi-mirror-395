# Flatgrep ⚡*Alpha v0.1.3*
> Automated searches for boring CLI tools.

Tired of typing by hand `flatpak run com.something.veryobnoxious`?  
Try **Flatgrep** for fuzzy search and grep what you want in just seconds. 

* **Quick test :** 
```bash
flatgrep run mpv
```

* **Fast and easy install apps from Flathub:**
```bash
flatgrep install firefox
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

| Action                          | Linux Command                          |
|---------------------------------|----------------------------------------|
| **Search on Flathub**           | `flatgrep search "app name" --flathub` |
| **List locally installed apps** | `flatgrep search "app name"`           |
| **Install an app from Flathub** | `flatgrep install "app name"`          |
| **Run an app**                  | `flatgrep run "app name"`              |
| **Uninstall an app**            | `flatgrep uninstall "app name"`        |

---

## Building Instructions 

#### Prerequisites

Before you begin, make sure you have the following installed on your system:
* Python 3.8+
* Flatpak
* `fzf` (a command-line fuzzy finder)

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
git clone git@github.com:rodhfr/flatgrep.git
cd flatgrep/src
```

#### Setup Python Virtual Environment 
```bash
# Create python virtual environment (isolated dependencies)
python -m venv .venv

# Activate the virtual python shell
source .venv/bin/activate # also works for zsh
#source .venv/bin/activate.fish # uncomment this line for fish shell

# Install python library requeriments
pip install -r requirements.txt
```

#### Install
```bash
# installation is just a binary in $HOME/.local/bin
sh build_and_install.sh
```

#### Uninstall
```bash
# Or just remove the binary located in $HOME/.local/bin
sh uninstall.sh
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
- [ ] Write installation guide.
- [ ] Release in some package manager.
- [ ] Write documentation.
- [ ] Search mode also searches by app names not only app ids.
- [ ] Run mode update: Auto install app if not available.
- [ ] Proper sanitize search command.

### Potential Features 🤔
- [ ] Other package managers like dnf/pacman/aur helpers.
