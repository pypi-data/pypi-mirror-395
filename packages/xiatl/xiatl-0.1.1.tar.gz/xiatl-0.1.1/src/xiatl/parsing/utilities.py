from xiatl.utilities import ensure
from pathlib import Path

def is_terminal(ast):

    return len(ast.children) == 1 and isinstance(ast.children[0], str)
            
def escape(value):

    escaped_value = (value
                     .replace("\\", "\\\\")
                     .replace("\n", r"\n")
                     .replace("\t", r"\t")
                     .replace("\f", r"\f")
                     .replace("\r", r"\r")
                     .replace("\b", r"\b")
                     .replace("\v", r"\v")
                     .replace("'", "\\'")
                     .replace('"', '\\"'))

    return escaped_value

def verify_initial_ast(ast):

    ensure(ast.name == "input")
    ensure(len(ast.children) == 2)
    ensure(ast.children[1].name == "PEG_EOF")

