from xiatl.parsing.pegboard.core.parse_node import *
from xiatl.parsing.pegboard.core.transforms import * 
from xiatl.parsing.pegboard.core.constants import *

def prefixed_transform(self):
    if self.children[0].name != "Prefix":
        return self.children[0]
    else:
        prefix = self.children[0]
        if prefix.children[0].name == "ASSERT":
            return Parse_Node("Assert", self.cursor_position, parent=self.parent, result=ACCEPTED, children=[self.children[1]])
        elif prefix.children[0].name == "REJECT":
            return Parse_Node("Reject", self.cursor_position, parent=self.parent, result=ACCEPTED, children=[self.children[1]])
        else:
            raise RuntimeError("unknown prefix")

def suffixed_transform(self):
    if self.children[-1].name != "Suffix":
        return self.children[-1]
    else:
        suffix = self.children[-1]
        if suffix.children[-1].name == "STAR":
            return Parse_Node("AtLeastZero", self.cursor_position, parent=self.parent, result=ACCEPTED, children=[self.children[0]])
        elif suffix.children[-1].name == "PLUS":
            return Parse_Node("AtLeastOne", self.cursor_position, parent=self.parent, result=ACCEPTED, children=[self.children[0]])
        elif suffix.children[-1].name == "QUESTION":
            return Parse_Node("Optional", self.cursor_position, parent=self.parent, result=ACCEPTED, children=[self.children[0]])
        else:
            raise RuntimeError("unknown suffix")

syntax_transforms = {
    "Identifier" : pool,
    "Comment"    : pool,
    "Pattern"    : sequential(pool, keep_chars(slice(1,-1))),
    "Primary"    : pass_through,
    "Spacing"    : drop,
    "OPEN"       : drop,
    "Expression" : pass_through,
    "Grouping"   : pass_through,
    "CLOSE"      : drop,
    "SLASH"      : drop,
    "LEFTARROW"  : drop,
    "Sequence"   : pass_through_if_single_child,
    "Choice"     : pass_through_if_single_child,
    "Prefixed"   : prefixed_transform,
    "Suffixed"   : suffixed_transform
}
