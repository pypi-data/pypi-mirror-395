from .transformer import AssignTransformer
from .patch import patch_and_reload_module

__all__ = ['custom_import']

origin_import = __import__


def custom_import(name, *args, **kwargs):
    module = origin_import(name, *args, **kwargs)
    if not hasattr(module, '__file__'):
        return module
    if module.__name__ == "warnings":
        return module
    try:
        patch_and_reload_module(module, trans=AssignTransformer)
    except:
        return module
    return module


__builtins__.update(**dict(
    __import__=custom_import
))
