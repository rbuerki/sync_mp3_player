import sys
from pathlib import Path

import pytest

# Append source code path to sys.path()
sys.path.append(str(Path.cwd().parent / "src"))
