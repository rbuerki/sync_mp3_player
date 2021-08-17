import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

FileDict = Dict[Path, datetime]
FileList = List[Path]


def walk_sync_dirs_and_merge_file_dicts(
    source: Path, target: Path, sync_dirs: List[str]
) -> Tuple[FileDict, FileDict]:
    """Get a dictionary each for the source and target containing
    all the files with their last modification date for the defined
    directories.
    """
    source_dict = target_dict = {}
    for sync_dir in sync_dirs:
        source_dict, target_dict = create_file_dicts(source, target, sync_dir)

        source_dict.update(source_dict)
        target_dict.update(target_dict)

    return source_dict, target_dict


def create_file_dicts(
    source: Path, target: Path, sync_dir: str
) -> Tuple[FileDict, FileDict]:
    """Create and return a new dict containing all file objects in
    the sync_dir on source and target, with the relative path as key
    and the timestamp of the last modification as value.
    """
    file_dicts = []
    for device in [source, target]:
        file_dict = {
            f.relative_to(device): f.stat().st_mtime
            for f in (device / sync_dir).rglob("*")
            if f.is_file()
        }
        file_dicts.append(file_dict)

    return file_dicts[0], file_dicts[1]


def compare_dicts(
    source_dict: FileDict, target_dict: FileDict,
) -> Tuple[FileList, FileList, FileList]:
    """Compare file dicts for and return a list each for all newly
    added, updated or deleted filepaths.
    """
    if source_dict == target_dict:
        added = removed = updated = []
        return added, removed, updated

    else:
        new_keys = set(source_dict.keys())
        old_keys = set(target_dict.keys())
        intersect_keys = new_keys.intersection(old_keys)
        added = list(new_keys - old_keys)
        updated = [f for f in intersect_keys if source_dict[f] > target_dict[f]]
        removed = list(old_keys - new_keys)

        return added, updated, removed


def copy_objects_to_target(file_list: FileList, source: Path, target: Path):
    """Copy objects in list from source to path. Existing objects
    will be overwritten.
    """
    for f in file_list:
        logging.info(f"Copying {f.name} to target ...")
        shutil.copy((source / f), (target / f))


def remove_objects_from_target(file_list: FileList, target: Path):
    """Delete objects in list from target. First the files,
    then all empty directories.
    """
    directories_to_delete_if_empty = []

    for f in file_list:
        logging.info(f"Deleting file {f.name} from target ...")
        (target / f).unlink()
        directories_to_delete_if_empty.append(f.parent)

    # Remove all empty directories
    for d in set(directories_to_delete_if_empty):
        try:
            logging.info(f"Removing empty directory {d} from target ...")
            d.rmdir()
        except OSError:
            pass
