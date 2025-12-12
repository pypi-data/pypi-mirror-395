import os
import importlib

# Get the directory of the current __init__.py file
current_directory = os.path.dirname(__file__)

# Iterate through all files in the current_directory
for filename in os.listdir(current_directory):
    # Check if the file is a Python file (ends with .py) and is not the current __init__.py
    if filename.endswith(".py") and not filename.startswith("__init__"):
        # Remove the .py extension from the filename to get the module name
        module_name = filename[:-3]

        # Import the module using importlib.import_module and add it to the globals dictionary
        module = importlib.import_module(f".{module_name}", package=__name__)
        globals().update({n: getattr(module, n) for n in module.__all__} if hasattr(module, '__all__') else {k: v for k, v in module.__dict__.items() if not k.startswith('_')})
