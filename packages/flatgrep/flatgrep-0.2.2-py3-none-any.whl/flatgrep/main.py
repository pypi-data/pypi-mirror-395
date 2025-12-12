# @Author: Rodolfo Souza
# Year = 2025
# Subject to copyright

#!/usr/bin/env python3
import sys, subprocess, re, pyperclip
from pyfzf.pyfzf import FzfPrompt
from rich.console import Console

console = Console()
fzf = FzfPrompt()

def run(cmd):
    return subprocess.run(cmd, text=True, capture_output=True).stdout.splitlines()

def pick(items, header):
    if not items:
        console.print("[red]Nothing to Show.[/]")
        sys.exit(1)

    sel = fzf.prompt(items, fzf_options=f"--header='{header}'")
    if not sel:
        console.print("[red]Abort.[/]")
        sys.exit(1)

    return sel[0]

def search_flatpaks(term, remote=False, skipfzf=False):
    cmd = (
        ["flatpak", "search", term, "--columns=application"]
        if remote
        else ["flatpak", "list", "--columns=application"]
    )

    lines = run(cmd)
    apps = [l.strip() for l in lines if l.strip()]
    filtered = [a for a in apps if term.lower() in a.lower()]

    if len(filtered) == 1:
        return filtered[0]

    if skipfzf:
        raise Exception("Skip fzf")

    return pick(filtered or apps, f"Choose '{term}' application id.")

def install(term):
    app = search_flatpaks(term, remote=True)
    try:
        result = subprocess.run(
            ["flatpak", "install", "flathub", app],
            text=True,
        )
        if result.returncode == 0:
            console.print(f"[green]Installed:[/] {app}")
            copycmd = f"flatpak run {app}"
            pyperclip.copy(copycmd)
            console.print(f"[blue]Copied to clipboard:[/] {copycmd}")
        else:
            console.print(f"[yellow]Installation cancelled by user[/]")
            pyperclip.copy(app)
            console.print(f"[blue]Copied to clipboard:[/] {app}")
    except Exception as e:
        console.print(f"[red]Error:[/] {e}")

    return app

def remove(term):
    app = search_flatpaks(term, remote=False)
    try:
        result = subprocess.run(
            ["flatpak", "remove", "-y", app],
            text=True,
        )
        if result.returncode == 0:
            console.print(f"[green]Removed:[/] {app}")
            pyperclip.copy(app)
            console.print(f"[blue]Copied to clipboard:[/] {app}")
    except Exception as e:
        console.print(f"[red]Error:[/] {e}")
    


def copy(term):
    app = search_flatpaks(term)
    pyperclip.copy(app)
    console.print(f"[blue]Copied to clipboard:[/] {app}")
    return app

def auto(term):
    try:
        app = search_flatpaks(term, remote=False, skipfzf=True)
        pyperclip.copy(app)
        console.print(f"[blue]Copied to clipboard:[/] {app}")
        return
    except Exception:
        pass
    app = install(term)

def main():
    if len(sys.argv) == 2:
        term = sys.argv[1]
        auto(term)
        return

    if len(sys.argv) < 3:
        console.print("[bold]Uso:[/] flat.py [install|remove|run|copy] app_id")
        sys.exit(1)

    action, term = sys.argv[1], sys.argv[2]

    if action == "install": install(term)
    elif action in ("remove", "uninstall"): remove(term)
    elif action == "run": run_app(term)
    elif action in ("copy", "search"): copy(term)
    else:
        console.print("[red]Invalid action[/]")

if __name__ == "__main__":
    main()

