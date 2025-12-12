#utils/cli_common.py
import sys
import subprocess
from .responses import Responses
from pyfzf.pyfzf import FzfPrompt

class CLICommon:
    @staticmethod
    def search_all(
            search_term: str,
            repo_name: str,
            command: list[str],
            parse_line,
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
        result = CLICommon.grep_fuzzy_fuzzyall(items, search_term, fzf_header)
        if result:
            Responses.copy_to_clipboard(result)
            return result

    @staticmethod
    def grep_fuzzy_fuzzyall(items: list[str], search_term: str, fzf_header: str | None = None):
        fzf = FzfPrompt()
        
        # First filter grep-like
        filtered = [item for item in items if search_term.lower() in item.lower()]
        
        # Case 1: one perfect match
        if len(filtered) == 1:
            output = filtered[0]
            Responses.search_term_found(output)
            return output
        
        # Case 2: multiple matches -> uses fzf
        if len(filtered) > 1:
            selection = fzf.prompt(filtered, fzf_options=f"--header '{fzf_header}'")
            if not selection: # user cancels
                Responses.exitprogram()
                return ""
            output = selection[0]
            Responses.search_term_found(output)
            return output
        
        # Case 3: matches none -> fzf all items 
        selection = fzf.prompt(items, fzf_options=f"--header '{fzf_header}'")
        if not selection:
            Responses.search_term_not_found(search_term)
            return ""
        output = selection[0]
        Responses.search_term_found(output)
        return output
    
    @staticmethod
    def run_command(command: list[str], sudo=False):
        subprocess.run(command)
    

    @staticmethod
    def exit_program():
        sys.exit(1)


