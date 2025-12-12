# cli/flatpak_cli.py
from utils.responses import Responses
from parsers.flatpak_parser import parse_flathub_lines
from parsers.flatpak_parser import parse_local_flatpaks_lines
from utils.cli_common import CLICommon

class FlatpakCLI:
    CLICommon = CLICommon() # only static functions in CLICommon() class none state is saved
    
    @staticmethod
    def search(search_term: str, flathub=False, installed=False, welcome=True):
        if welcome:
            Responses.welcome_mode("flatpak search")

        if flathub:
            repo_name="flathub"
            command=["flatpak", "search", search_term]
            parser=parse_flathub_lines
        else:
            repo_name="locally installed flatpaks"
            command=["flatpak", "list"]
            parser=parse_local_flatpaks_lines

        return CLICommon.search_all(
            search_term,
            repo_name=repo_name,
            command=command,
            parse_line=parser,
            fzf_header=f"Fuzzy searching {repo_name} with '[{search_term}]'"
        )
    
    @staticmethod
    def _execute(action: str, search_term: str, flathub=False):
        Responses.welcome_mode(f"flatpak {action}")
        
        command = None
        flatpak_app_id = FlatpakCLI.search(search_term, flathub, welcome=False)
        if not flatpak_app_id:
            print(f"❌ No Flatpak app found for '{search_term}'")
            return
        if action == "install":
            command = ["flatpak", "install", "flathub", flatpak_app_id]
        elif action in ["uninstall", "remove"] :
            command = ["flatpak", "remove", flatpak_app_id]
        elif action == "run":
            command = ["flatpak", "run", flatpak_app_id]
        if command is None:
            print(f"❌Unknown action '{action}")
            return
        try:
            CLICommon.run_command(command)
            print(f"✅ Successfully executed '{action}' on '{flatpak_app_id}'")
        except Exception as e:
            print(f"❌ Error running '{action}' on '{flatpak_app_id}': {e}")

    @staticmethod
    def uninstall(search_term: str):
        FlatpakCLI._execute("remove", search_term)

    @staticmethod
    def remove(search_term: str):
        FlatpakCLI._execute("remove", search_term)
    
    @staticmethod
    def run(search_term: str):
        FlatpakCLI._execute("run", search_term)

    @staticmethod
    def install(search_term: str, flathub=True):
        FlatpakCLI._execute("install", search_term, flathub)
