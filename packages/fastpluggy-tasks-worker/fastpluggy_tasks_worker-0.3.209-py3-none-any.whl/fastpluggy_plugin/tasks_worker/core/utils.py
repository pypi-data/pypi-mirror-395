# tasks/utils.py
import importlib
from typing import Callable


def func_to_path(func: Callable | str) -> str:
    """
    Return a stable identifier for a function.
    - For callables: "<module>:<qualname>"
    - For strings: returned as-is (supports simple names, "module.qualname" or "module:qualname")
    """
    if isinstance(func, str):
        return func
    module = getattr(func, "__module__", None) or "__main__"
    qualname = getattr(func, "__qualname__", None) or getattr(func, "__name__", str(func))
    return f"{module}:{qualname}"

def path_to_func(path: str) -> Callable:
    mod, name = path.split(":", 1)
    module = importlib.import_module(mod)
    obj = module
    for part in name.split("."):
        obj = getattr(obj, part)
    return obj

def it_allow_concurrent(func: Callable) -> bool:
    """
    Return True if the task function allows concurrent execution.
    """
    meta = getattr(func, "_task_metadata", {})
    return meta.get("allow_concurrent", True)

def get_task_type(func) -> str:
    task_type = "native"  # default
    if isinstance(func, str):
        # If func is a string path, try to retrieve it from registry to get metadata
        from ..registry.registry import task_registry
        registered_func = task_registry.get(func)
        if registered_func and hasattr(registered_func, "_task_metadata"):
            task_type = registered_func._task_metadata.get("task_type", "native")
    elif hasattr(func, "_task_metadata"):
        # Func is a callable with metadata
        task_type = func._task_metadata.get("task_type", "native")
    return task_type
