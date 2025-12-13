"""
A utility to dynamically load template dictionaries from modules in a given package.
"""

import importlib
import os
from typing import Any


def load_templates_from_path(path: str) -> dict[str, Any]:
    """
    Loads all TEMPLATE dictionaries from Python files in the given directory.

    Args:
        path: Filesystem path to the directory containing template modules.

    Returns:
        A dictionary mapping filename (without .py) to the TEMPLATE dict in each file.
    """
    templates = {}
    abs_path = os.path.abspath(path)
    for filename in os.listdir(abs_path):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            file_path = os.path.join(abs_path, filename)
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if not spec or not spec.loader:
                continue
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "TEMPLATE"):
                templates[module_name] = module.TEMPLATE
    return templates
