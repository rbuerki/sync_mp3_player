import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

logger = logging.getLogger(__name__)

FileDict = Dict[Path, datetime]
FileList = List[Optional[Path]]


# def find_last_modified_file(sync_dir_path):
#     """TODO: just for testing. Rewrite to return_last_modification_date()."""
#     time, file_path = max(
#         (f.stat().st_mtime, f) for f in sync_dir_path.rglob("*")
#     )
#     print(datetime.fromtimestamp(time), file_path)


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
        # logging.debug(f"{device}, {sync_dir}, {len(file_dict.items())}")  # TODO remove
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
            f"No changes detected between target and source "
            f"for directory '{sync_dir}''."
        )
        added = removed = updated = []
        return added, removed, updated

    else:
        new_keys = set(source_dict.keys())
        old_keys = set(target_dict.keys())
        intersect_keys = new_keys.intersection(old_keys)
        added = list(new_keys - old_keys)
        removed = list(old_keys - new_keys)
        updated = [f for f in intersect_keys if source_dict[f] > target_dict[f]]

        # # Pretify the output if len of object is 0
        # for iterable in [added, removed, updated]:
        #     if len(iterable) == 0:
        #         iterable = "-"
        #     else:
        #         iterable = ", ".join([f.name for f in iterable])

        logger.warning(
            "[dark_red]CHANGES DETECTED in tables and / or views since last run[/]:\n"
            f"- Added files: {added if len(added) > 0 else '-'}\n"
            f"- Removed files: {removed if len(removed) > 0 else '-'}\n"
            f"- Updated files: {updated if len(updated) > 0 else '-'}."
        )
        return added, removed, updated


def copy_objects_to_target(
    file_list: FileList, source: Path, target: Path, sync_dir: str
) -> int:
    """Copy objects in list from source to path. Existing objects will be overwritten."""
    counter = 0
    for f in file_list:
        logging.info(f"Copying {f} to target ...")
        shutil.copy((source / sync_dir / f), (target / sync_dir / f))
        counter += 1
    return counter


def remove_objects_from_target(
    file_list: FileList, target: Path, sync_dir: str
) -> int:
    """Delete objects in list from target."""
    counter = 0
    for f in file_list:
        logging.info(f"Deleting {f} from target ...")
        (target / sync_dir / f).unlink()
        counter += 1
    return counter
