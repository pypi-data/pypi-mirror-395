# tools/loader.py
import importlib
import pkgutil
from typing import Callable
import mcp_server_stdio.tools as package

def load_tools(mcp):
    for _, module_name, _ in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        module = importlib.import_module(module_name)
        register: Callable = getattr(module, "register", None)
        if callable(register):
            register(mcp)
