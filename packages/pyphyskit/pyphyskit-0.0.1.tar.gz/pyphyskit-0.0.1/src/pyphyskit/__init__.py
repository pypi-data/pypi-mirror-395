
__version__="0.0.1"

import importlib
import pkgutil
import sys

package_name = "pyphyskit"

for loader, module_name, is_pkg in pkgutil.iter_modules(__path__):
    full_module_name = f"{package_name}.{module_name}"
    module = importlib.import_module(full_module_name)
    for attr in dir(module):
        if not attr.startswith("_"):
            globals()[attr] = getattr(module, attr)
