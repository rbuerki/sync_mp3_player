import logging
import yaml
from pathlib import Path
from typing import Dict, Optional, Union

logger = logging.getLogger(__name__)


def read_yaml(file_path: Union[str, Path], section: Optional[str]) -> Dict:
    """Return the key-value-pairs from a YAML file, or, if the
    optional `section` parameter is passed, only from a specific
    section of that file.
    """
    with open(file_path, "r") as f:
        yaml_content = yaml.safe_load(f)
    if not section:
        return yaml_content
    else:
        try:
            return yaml_content[section]
        except KeyError:
            logging.error(
                f"Section {section} not found in config file. Please check."
            )
            raise
