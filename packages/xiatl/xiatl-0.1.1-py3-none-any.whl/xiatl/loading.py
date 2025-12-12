from pathlib import Path
import re
from xiatl.parsing import parse_string
from xiatl.processing import process_string, finalize_local_tree, finalize_project_tree
from xiatl.resolution import resolve_file, resolve_string, _resolve_string
from xiatl.errors import *
from xiatl.constants import FILE_EXTENSION, PROJECT_ROOT, LOCAL_ROOT
from xiatl.utilities import ensure
from xiatl.node import Node

def load_project(dirname, debug=False):
    return _load_project(dirname, debug=debug, is_top=True)

def _load_project(dirname, debug=False, is_top=False):
    path = Path(dirname)
    dirname_stem = path.stem

    if not path.exists():
        raise Loading_Error(f"Path does not exist: {path}")

    if not path.is_dir():
        raise Loading_Error(f"Path is not a directory: {path}")

    try:
        paths = list(path.iterdir())
    except Exception as e:
        raise Loading_Error(f"Failed to read '{path}'") from e

    children = []
    for p in paths:
        if p.is_file() and p.suffix == FILE_EXTENSION:
            try:
                children.append(load_file(str(p)))
            except Exception as e:
                raise Loading_Error(f"failed to load file '{str(p)}'") from e
        elif p.is_dir():
            try:
                children.append(_load_project(str(p)))
            except Exception as e:
                raise Loading_Error(f"failed to directory '{str(p)}'") from e

    if is_top:
        project_root = Node(node_type=PROJECT_ROOT, name=dirname_stem, children=children)
        finalize_project_tree(node=project_root, project_root=project_root)
        return project_root
    else:
        return Node(node_type=LOCAL_ROOT, name=dirname_stem, children=children)

def load_file(filename, debug=False):

    if not isinstance(debug, bool):
        raise ValueError("debug must be of type 'bool'")

    if not isinstance(filename, str):
        raise ValueError("filename must be of type 'str'")

    path = Path(filename)
    filename_stem = path.stem

    if path.suffix != FILE_EXTENSION:
        raise ValueError(f"Invalid filename: '{filename}'\nFilename must end with {FILE_EXTENSION}.")

    if not re.fullmatch(r"\w+", filename_stem):
        raise ValueError(f"Invalid filename stem: '{filename_stem}'\nFilename stem must contain only alphanumeric or underscore characters.")

    with open(filename, "r", encoding="utf-8") as f:
        input_string = f.read()

    return _load_input(input_string=input_string, name=filename_stem, error_message="Invalid input file", debug=debug)

def load_string(input_string, name=None, debug=False):

    if not isinstance(debug, bool):
        raise ValueError("debug must be of type 'bool'")

    if not isinstance(input_string, str):
        raise ValueError("input_string must be of type 'str'")

    if name is not None:
        if not isinstance(name, str):
            raise ValueError(f"Invalid name: '{name}'\nName must be of type 'str'.")
        if not re.fullmatch(r"[\w\s]+", name):
            raise ValueError(f"Invalid name: '{name}'\nName must contain only alphanumeric, underscore characters, or whitespace.")

    return _load_input(input_string=input_string, name=name, error_message="Invalid input string", debug=debug)

def _load_input(input_string, name, error_message, debug):

    resolved_input_string = _resolve_string(input_string, debug=debug, error_message=error_message)
    local_root = process_string(resolved_input_string, name=name, error_message=error_message)
    finalize_local_tree(node=local_root, local_root=local_root)

    return local_root



