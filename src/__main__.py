import logging
from datetime import datetime
from pathlib import Path
from typing import List, SupportsRound

from rich.console import Console
from rich.logging import RichHandler

import utils
import foos

console = Console()

CONFIG_PATH = Path.cwd() / "config.yaml"


def initialize_logger():
    """Initialize logging to console using rich."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # Create a formatter
    cformatter = logging.Formatter(fmt="%(message)s", datefmt="[%X]")
    # Create console handler
    sh = RichHandler(show_time=False, show_path=False, markup=True)
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(cformatter)
    logger.addHandler(sh)

    return logger


# TEST
def main(logger: logging.Logger):

    source: Path = Path(utils.read_yaml(CONFIG_PATH, "SOURCE_PATH"))
    target: Path = Path(utils.read_yaml(CONFIG_PATH, "TARGET_PATH"))
    sync_dirs: List[str] = utils.read_yaml(CONFIG_PATH, "SYNC_DIRECTORIES")

    logger.info("\n[bold DARK_MAGENTA]STARTING SYNC PROCESS ...[/]",)

    for sync_dir in [sync_dirs[0]]:  # TODO testing
        source_dict, target_dict = foos.create_file_dicts(
            source, source, sync_dir
        )
        added, removed, updated = foos.compare_dicts(source_dict, target_dict)

        print(added, removed, updated)

        # sync_dir_path = source / dir
        # if sync_dir_path.exists():
        #     foos.find_last_modified_file(sync_dir_path)


if __name__ == "__main__":
    logger = initialize_logger()
    main(logger)
