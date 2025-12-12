import sys
import subprocess
import fire
import pyperclip
import re
from pyfzf.pyfzf import FzfPrompt
from rich.console import Console

fzf = FzfPrompt()
console = Console()

class Responses:
    @staticmethod
    def search_term_found(term): 
        console.print(f"[bold blue]Search term found: [bold green]{term}[/][/]")

    @staticmethod
    def search_term_not_found(term):
        console.print("[bold red]No item selected. Abort.[/]")

    @staticmethod
    def copy_to_clipboard(item):
        item_str = item[0] if isinstance(item, list) else item
        pyperclip.copy(item_str)
        console.print(f"[bold blue]:clipboard:ID copied to clipboard :clipboard:[/]")

    @staticmethod
    def search_indicator(term, repo):
        console.print(f"[bold blue]:mag:Searching '[bold yellow]{term}[/]' in '[bold yellow]{repo}[/]' repository...[/]")
    
    @staticmethod
    def welcome_mode(mode):
        console.print(f":package: [bold black on green]{mode.upper()}[/bold black on green] [bold white]CLI Mode[/]")

    @staticmethod
    def exitprogram():
        console.print(f"[bold red]Search term not found. Exiting...[/bold red]")
        sys.exit(1)
            
class CLICommon:
    @staticmethod
    def search_all(
            search_term: str,
            repo_name: str,
            command: list[str],
            parse_line: callable,
            fzf_header: str
    ):

        Responses.search_indicator(search_term, repo_name)
        items = []
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, errors = proc.communicate()

        for line in output.splitlines():
            item = parse_line(line)
            if item:
                items.append(item)
        result = ParseTools.grep_fuzzy_fuzzyall(items, search_term, fzf_header)
        if result:
            Responses.copy_to_clipboard(result)
            return result




class DNFCLI:
    def search(self, search_term: str, installed=False):
        Responses.welcome_mode("dnf")
        if not installed:
            CLICommon.search_all(
                    search_term,
                    repo_name="dnf",
                    command=["dnf", "search", search_term],
                    parse_line=lambda line: re.match(r'^\s*([^\s:]+)', line).group(1) if re.match(r'^\s*([^\s:]+)', line) else None,
                    fzf_header=f"Fuzzy searching dnf packages with [{search_term}]"
            )


class FlatpakCLI:
    def search(self, search_term: str, flathub=False, installed=False):
        Responses.welcome_mode("flatpak")

        if flathub:
            CLICommon.search_all(
                    search_term,
                    repo_name="flatpak",
                    command=["flatpak", "search", search_term],
                    parse_line=lambda line: re.split(r'\t+', line)[2] if len(re.split(r'\t+', line)) > 2 else None,
                    fzf_header=f"Fuzzy searching flatpak apps with "
            )

        elif installed:
            self._search_flatpak_installed(search_term)
        else:   
            self._search_flatpak_installed(search_term)

    def _search_flatpak_installed(self, search_term, fzf_header="Fuzzy searching installed flatpaks with"):
        repo = "installed"
        flatpak_ids = []

        Responses.search_indicator(search_term, repo)

        # Running search command with subprocess
        flatpak_installed = subprocess.Popen(["flatpak", "list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, errors = flatpak_installed.communicate()

        # Specific parsing for flatpak search output
        for line in output.splitlines():
            match = re.split(r'\t+', line)
            #print(match[1]) # print each line of the match
            flatpak_ids.append(match[1])
        
        result = ParseTools.grep_fuzzy_fuzzyall(flatpak_ids, search_term, fzf_header)
        if result:
            Responses.copy_to_clipboard(result)
            return result

class CLI:
    flatpak = FlatpakCLI()
    dnf = DNFCLI()

class ParseTools:
    @staticmethod
    def grep_fuzzy_fuzzyall(items: list[str], search_term: str, fzf_header: str | None = None) -> str:
        filtered_ids = [item for item in items if search_term.lower() in item.lower()]
        
        # fuzzy find search_term
        if filtered_ids:
            if len(filtered_ids) == 1:
                output = filtered_ids[0]
            elif len(filtered_ids) > 1:
                output = fzf.prompt(filtered_ids, fzf_options=f"--header \"{fzf_header} [{search_term}]\"")
                if not output:
                    console.print("[bold red]Nenhum item selecionado. Abortando.[/]")
                    return None  

            Responses.search_term_found(output)
            return output

        # if no search_term found, search from all ids
        output = fzf.prompt(items, fzf_options=f"--header '{fzf_header} [{search_term}]'")
        Responses.search_term_found(output)
        return output

    def parse_flatpak_line(line):
        parts = re.split(r'\t+', line)
        if len(parts) > 2:
            return parts[2]
        else:
            Responses.exitprogram()

if __name__ == "__main__":
    fire.Fire(CLI)

