# main.py
from cli.dnf_cli import DNFCLI
from cli.flatpak_cli import FlatpakCLI
import fire

class CLI(FlatpakCLI):
    pass
    # #dnf = DNFCLI() # in development
    # flatpak = FlatpakCLI()

if __name__ == "__main__":
    fire.Fire(CLI)
