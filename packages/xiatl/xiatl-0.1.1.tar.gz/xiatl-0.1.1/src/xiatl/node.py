from xiatl.utilities import ensure
from xiatl.parsing.utilities import escape
from xiatl.node_reference import Node_Reference 

class Node:

    def __init__(self, node_type, name=None, tags=None, children=None):

        ensure(isinstance(node_type, str))
        ensure(name is None or isinstance(name, str))

        if tags is None:
            tags = []

        ensure(isinstance(tags, list))

        for tag in tags:
            ensure(isinstance(tag, str))

        if children is None:
            children = []

        ensure(isinstance(children, list))

        for child in children:
            ensure(isinstance(child, str) or child.__class__.__name__ == "Node" or isinstance(child, Node_Reference))

        self.node_type = node_type
        self.name = name
        self.tags = tags
        self.children = children
        self.parent = None

    def __str__(self):

        s = f"{self.node_type} "

        if self.name is not None:
            s += f"[{self.name}] "

        if len(self.tags) > 0:
            s += "{"
            for i in range(len(self.tags)-1):
                s += f"{self.tags[i]}, "

            s += f"{self.tags[-1]}"
            s += "} "

        s += "< "
        for child in self.children:
            s += str(child) + " "

        s += " >"

        return s

    def __repr__(self):

        return self.__class__.__name__ + f"(type={self.node_type},name={self.name},tags={self.tags},children={self.children})"

    def to_string(self, depth=0, indentation_space_count=3):

        s = " " * indentation_space_count * depth + f"{self.node_type}"

        if self.name is not None:
            s += f" [{self.name}]"

        if len(self.tags) > 0:
            s += " {"
            for i in range(len(self.tags)-1):
                s += f"{self.tags[i]}, "
            s += f"{self.tags[-1]}"
            s += "}"

        if len(self.children) > 0:
            s += " <\n"

            for child in self.children:
                if isinstance(child, str):
                    s += " " * indentation_space_count * (depth+1) + escape(child) + "\n"
                else:
                    s += child.to_string(depth=depth+1, indentation_space_count=indentation_space_count)
        else:
            s += " <>\n"

        return s
