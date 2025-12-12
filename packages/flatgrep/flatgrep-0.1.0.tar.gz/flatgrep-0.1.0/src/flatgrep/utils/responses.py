#utils/responses.py
import sys
import pyperclip
from rich.console import Console

console = Console()
class Responses:

    @staticmethod
    def search_term_found(term): 
        console.print(f"[bold blue]Search term found: [bold green]{term}[/][/]")

    @staticmethod
    def search_term_not_found(term):
        console.print(f"[bold red]Search term not found: '{term}'[/]")
    
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
        console.print(f"[bold red] No item selected. Abort. [bold red]")
        sys.exit(1)

