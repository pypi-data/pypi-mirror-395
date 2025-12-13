import typing as t
from pathlib import Path

from .exceptions import XcdoError
from .io_utils import open_dataset


def input_file_validator(path: str) -> str:
    if not Path(path).exists():
        raise XcdoError(f"File {path} does not exist")
    return path


def path_to_dataset_validator(path: t.Any) -> t.Any:
    if isinstance(path, str):
        return open_dataset(path)
    return path


def output_file_validator(path: str) -> str:
    parent = Path(path).parent
    if not parent.exists():
        raise XcdoError(f"Directory {parent} does not exist")
    return path
