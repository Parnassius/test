from typing import Callable, Dict

from os.path import dirname, basename, isfile, join
import glob
import importlib

modules = glob.glob(join(dirname(__file__), "*.py"))

plugins: Dict[str, Callable] = {}

for f in modules:
    if isfile(f) and not f.endswith("__init__.py"):
        name = basename(f)[:-3]
        m = importlib.import_module("plugins." + name)
        plugins.update(m.commands)  # type: ignore
