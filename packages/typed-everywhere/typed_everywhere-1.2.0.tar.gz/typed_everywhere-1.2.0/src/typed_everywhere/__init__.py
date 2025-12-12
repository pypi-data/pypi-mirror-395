import assign_overload
from .typed_everywhere import Typed, typed_method

def __getattr__(name):
    if name == "patch_and_reload_module":
        return assign_overload.patch_and_reload_module
    else:
        raise AttributeError(f"module {__name__} has no attribute {name}")
