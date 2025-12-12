from xiatl.parsing.parser import *
def parse_string(string):
    result = parser.parse_string(string)
    if result.accepted:
        result.apply_transforms(xiatl_transforms)
    return result

