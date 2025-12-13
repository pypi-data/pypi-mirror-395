import os
import sys
from pathlib import Path
from signal import SIGINT, signal

from .cli import Main


# noinspection PyUnresolvedReferences,PyProtectedMember
def signal_handler(*args):
    os._exit(1)

def main():
    signal(SIGINT, signal_handler)
    cwd_folder = Path(__name__).resolve().parent

    try:
        github_token = os.environ["GITHUB_TOKEN"]
    except KeyError:
        github_token = None

    Main.set_default_args(root_folder=cwd_folder, github_token=github_token)
    sys.exit(Main.exec())

if __name__ == "__main__":
    main()