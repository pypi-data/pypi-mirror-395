# cli/dnf_cli.py
from utils.cli_common import CLICommon
from utils.responses import Responses
from parsers.dnf_parser import parse_dnf_lines

class DNFCLI:
    CLICommon = CLICommon()
    def search(self, search_term: str, installed=False):
        Responses.welcome_mode("dnf")

        if installed:
            pass
        else:
            repo_name="public dnf packages"
            command=["dnf", "search", search_term]
            parser=parse_dnf_lines

            CLICommon.search_all(
                    search_term,
                    repo_name=repo_name,
                    command=command,
                    parse_line=parser,
                    fzf_header=f"Fuzzy searching {repo_name} with '[{search_term}]'"
            )



