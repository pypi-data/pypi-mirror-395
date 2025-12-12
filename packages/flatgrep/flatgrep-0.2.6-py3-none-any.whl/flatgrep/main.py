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
    try: 
        app = search_flatpaks(term, remote=False, skipfzf=True)
        console.print(f"[green]Already installed:[/] {app}")
        pyperclip.copy(app)
        console.print(f"[blue]Copied to clipboard:[/] {app}")
        return app
    except Exception:
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
    
def list_all():
    cmd = (
        ["flatpak", "list", "--columns=application"]
    )

    lines = run(cmd)
    apps = [l.strip() for l in lines if l.strip()]

    if not apps:
        console.print("[red]No applications installed.[/]")
        return

    sel_app = pick(apps, f"Choose application id.")
    pyperclip.copy(sel_app)
    console.print(f"[blue]Copied to clipboard:[/] {sel_app}")

def copy(term):
    app = search_flatpaks(term)
    pyperclip.copy(app)
    console.print(f"[blue]Copied to clipboard:[/] {app}")
    return app

def run_app(term):
    app = search_flatpaks(term)
    try:
        subprocess.run(["flatpak", "run", app])
    except Exception as e:
        console.print(f"[red]Error running {app}:[/] {e}")

def auto(term):
    app = install(term)

def main():
    if len(sys.argv) < 2:
        console.print("[bold]Usage:[/] flat.py \[install|remove|run|copy|list\] app_id")
        sys.exit(1)

    action = sys.argv[1]

    # Named Commands
    if action == "install" and len(sys.argv) >= 3:
        term = " ".join(sys.argv[2:])
        install(term)
    elif action in ("remove", "uninstall") and len(sys.argv) >= 3:
        term = " ".join(sys.argv[2:])
        remove(term)
    elif action == "run" and len(sys.argv) >= 3:
        term = " ".join(sys.argv[2:])
        run_app(term)
    elif action in ("copy", "search") and len(sys.argv) >= 3:
        term = " ".join(sys.argv[2:])
        copy(term)
    elif action == "list":
        list_all()
    else:
        term = " ".join(sys.argv[1:])
        auto(term)

if __name__ == "__main__":
    main()

