from datetime import datetime
from pathlib import Path
from typing import List


import utils

CONFIG_PATH = Path.cwd() / "config.yaml"

source_path = Path(utils.read_yaml(CONFIG_PATH, "SOURCE_PATH"))
target_path = Path(utils.read_yaml(CONFIG_PATH, "TARGET_PATH"))
sync_dirs = utils.read_yaml(CONFIG_PATH, "SYNC_DIRECTORIES")


def find_last_modified_file(sync_dir_path):
    """TODO: just for testing. Rewrite to return_last_modification_date()"""
    time, file_path = max(
        (f.stat().st_mtime, f) for f in sync_dir_path.rglob("*")
    )
    print(datetime.fromtimestamp(time), file_path)


def list_newly_modified_objects(sync_dir_path: Path, last_modification_date: datetime) -> List[Path]:
    """TODO"""
    pass


def copy_objects_to_target(sync_dir_path: Path, ...) -> int:
    """TODO"""
    counter = 0
    return counter


def find_removed_objects(sync_dir_path: Path, ...) -> List[Path]:
    """TODO"""
    pass


def delete_removed_objects_on_target():
    """TODO"""
    pass


# SMALL TEST

for dir in sync_dirs:
    sync_dir_path = source_path / dir
    if sync_dir_path.exists():
        find_last_modified_file(sync_dir_path)
