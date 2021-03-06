from pathlib import Path
from typing import List

from rich.console import Console

import utils
import foos

console = Console()

CONFIG_PATH = Path.cwd() / "config.yaml"


def main(console: Console):

    source: Path = Path(utils.read_yaml(CONFIG_PATH, "SOURCE_PATH"))
    target: Path = Path(utils.read_yaml(CONFIG_PATH, "TARGET_PATH"))
    sync_dirs: List[str] = utils.read_yaml(CONFIG_PATH, "SYNC_DIRECTORIES")

    console.log("[bold yellow]Starting sync process ...[/]",)

    foos.check_and_prepare_target(target, sync_dirs)
    source_dict, target_dict = foos.walk_sync_dirs_and_merge_file_dicts(
        source, target, sync_dirs
    )
    added, updated, removed = foos.compare_dicts(source_dict, target_dict)

    console.print(
        f"\n[magenta] - Found {len(added)} new files."
        f"\n - Found {len(updated)} updated files."
        f"\n - Found {len(removed)} removed files.\n"
    )

    if len(added) > 0:
        foos.copy_objects_to_target(added, source, target)
    if len(updated) > 0:
        foos.copy_objects_to_target(updated, source, target)
    if len(removed) > 0:
        dirs_to_delete = foos.remove_files_from_target(removed, target)
        foos.remove_empty_directories_from_target(dirs_to_delete)

    console.log("[bold yellow] Sync process complete!")


if __name__ == "__main__":
    main(console)
