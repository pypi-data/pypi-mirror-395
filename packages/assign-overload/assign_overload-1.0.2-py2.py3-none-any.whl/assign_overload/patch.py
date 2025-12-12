import ast
import sys
from .transformer import AssignTransformer


__all__ = [
    'patch_node_ast',
    'patch_code_ast',
    'patch_file_ast',
    'patch_module_ast',
    'patch_and_reload_module'
]


def patch_node_ast(node, trans=AssignTransformer):
    trans = trans()
    new_node = trans.visit(node)
    ast.fix_missing_locations(new_node)
    return new_node


def patch_code_ast(code_str, trans=AssignTransformer):
    code_ast = ast.parse(code_str)
    return patch_node_ast(code_ast, trans)


def patch_file_ast(filename, trans=AssignTransformer):
    with open(filename, "r") as f:
        code_str = ''.join(f.readlines())
        return patch_code_ast(code_str, trans)


def patch_module_ast(module, trans=AssignTransformer):
    if not hasattr(module, '__file__'):
        return module
    filename = module.__file__.replace('.pyc', '.py')
    return patch_file_ast(filename, trans)


def patch_and_reload_module(module = None, trans=AssignTransformer):
    if module is None:
        module_name = sys._getframe(1).f_globals["__name__"]
        module = sys.modules[module_name]    
    if not hasattr(module, "patched") or not module.patched:
        module.patched = True
        patched_ast = patch_module_ast(module)
        module.modified_source = ast.unparse(patched_ast)
        patched_code = compile(patched_ast, module.__name__, "exec")
        module.executing_patch = True
        exec(patched_code, module.__dict__)
        module.executing_patch = False
    return module.executing_patch
