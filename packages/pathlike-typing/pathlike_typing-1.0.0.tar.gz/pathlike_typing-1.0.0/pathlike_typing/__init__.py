from typing import Union
from pathlib import Path

__version__ = "1.0.0"
PathLike = Union[Path, str]
__all__ = ["PathLike", "__version__"]
