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

def is_terminal(node):
    if len(node.children) == 1 and isinstance(node.children[0], str):
        return True
    else:
        return False

