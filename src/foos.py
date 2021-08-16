import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

logger = logging.getLogger(__name__)

FileDict = Dict[Path, datetime]
FileList = List[Optional[Path]]


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
            f.relative_to(device / sync_dir): f.stat().st_mtime
            for f in (device / sync_dir).rglob("*")
            if f.is_file()
        }
        file_dicts.append(file_dict)

    return file_dicts[0], file_dicts[1]


def compare_dicts(
    source_dict: FileDict, target_dict: FileDict, sync_dir: str,
) -> Tuple[FileList, FileList, FileList]:
    """Compare file dicts for and return a list each for all newly
    added, updated or deleted filepaths.
    """
    if source_dict == target_dict:
        logger.info(
            f"[yellow]No changes detected between target and source "
            f"for directory '{sync_dir}'.[/]"
        )
        added = removed = updated = []
        return added, removed, updated

    else:
        new_keys = set(source_dict.keys())
        old_keys = set(target_dict.keys())
        intersect_keys = new_keys.intersection(old_keys)
        added = list(new_keys - old_keys)
        updated = [f for f in intersect_keys if source_dict[f] > target_dict[f]]
        removed = list(old_keys - new_keys)

        logger.warning(
            f"[yellow]Changes dected between target and source"
            f"for directory '{sync_dir}':[/]\n"
            f"- Added files: {added if len(added) > 0 else '-'}\n"
            f"- Removed files: {removed if len(removed) > 0 else '-'}\n"
            f"- Updated files: {updated if len(updated) > 0 else '-'}."
        )
        return added, updated, removed


def copy_objects_to_target(
    file_list: FileList, source: Path, target: Path, sync_dir: str
) -> int:
    """Copy objects in list from source to path. Existing objects
    will be overwritten.
    """
    counter = 0
    for f in file_list:
        logging.info(f"Copying {f} to target ...")
        shutil.copy((source / sync_dir / f), (target / sync_dir / f))
        counter += 1
    return counter


def remove_objects_from_target(
    file_list: FileList, target: Path, sync_dir: str
) -> int:
    """Delete objects in list from target. First the files,
    then all empty directories.
    """
    directories_to_delete_if_empty = []
    counter = 0

    for f in file_list:
        logging.info(f"Deleting file {f} from target ...")
        (target / sync_dir / f).unlink()
        directories_to_delete_if_empty.append(f.parent)
        counter += 1

    # Remove all empty directories
    for d in set(directories_to_delete_if_empty):
        try:
            logging.info(f"Removing empty directory {d} from target ...")
            d.rmdir()
        except OSError:
            pass

    return counter
