from xiatl.parsing.pegboard.core.utilities import *

def drop_if_no_child(self):
    if len(self.children) == 0:
        return None
    else:
        return self

def pass_through_if_single_child(self):
    if len(self.children) == 1:
        if not isinstance(self.children[0], str):
            self.children[0].parent = self.parent
        return self.children[0]
    else:
        return self

def rename(new_name):
    def f(self):
        self.name = new_name
        return self
    return f

def pool(self):
    cursor_position = None
    result = ""
    for child in self.children:
        if not is_terminal(child):
            raise ValueError(f"'pool' cannot be used with non-terminal node {child} of {self}")
        result += child.children[0]
    self.children = [result]
    return self

def pass_through(self):
    if len(self.children) == 1:
        if not isinstance(self.children[0], str):
            self.children[0].parent = self.parent
        return self.children[0]
    elif len(self.children) == 0:
        return None
    else:
        raise ValueError(f"'pass_through' should only be used on nodes with a single child, not {len(self.children)} as has {self}")

def drop(self):
    return None

def keep_chars(s):
    def f(self):
        if len(self.children) != 1 or (not isinstance(self.children[0], str)):
            raise ValueError("'keep_chars' can only be used with terminal nodes (i.e., nodes with only a single child and of type 'str')")
        self.children[0] = self.children[0][s]
        return self
    return f

def sequential(*transforms):
    if len(transforms) < 1:
        raise ValueError("'sequential' must be provided at least one function to apply")
    def f(self):
        for transform in transforms:
            self = transform(self)
        return self
    return f


