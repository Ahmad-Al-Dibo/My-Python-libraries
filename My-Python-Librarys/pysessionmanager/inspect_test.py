import inspect
import pysessionmanager.core as core

def list_functions(module):
    functions = inspect.getmembers(module, inspect.isfunction)
    classes = inspect.getmembers(module, inspect.isclass)
    for name, func in functions:
        print(f"Function: {name}")
    for name, func in classes:
        print(f"Class: {name}")

list_functions(core)