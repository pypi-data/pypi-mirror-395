from xiatl.parsing.pegboard.core.constants import *
from xiatl.parsing.pegboard.core.utilities import *

def generate_dummy_node(name=None, children=None):
    if name is None:
        name = "_dummy_node"
    if children is None:
        children = []
    return Parse_Node(name=name, cursor_position=(-1,-1), result=ACCEPTED, children=children)

class Parse_Node:

    def __init__(self, name, cursor_position, parent=None, result=None, children=None, raw_cursor_position=None):

        self.raw_cursor_position=raw_cursor_position
        self.parent = parent
        self.cursor_position = cursor_position
        self.name = name
        self.result = result

        if children is None:
            self.children = []
        else:
            self.children = children # list(Parse_Node | str) or None

    def __repr__(self):
        return self.__class__.__name__ + f"(name={self.name},cursor_position={self.cursor_position},result={self.result},children={self.children})"

    def branch_to_string(self, show_position=True, show_result=True, indentation_space_count=1):

        branch = []
        current_node = self

        while current_node is not None:
            branch.append(current_node)
            current_node = current_node.parent

        s = ""

        for i, node in enumerate(reversed(branch)):
            s += i * " " * indentation_space_count
            s += node.to_string(show_position=show_position,
                                show_result=show_result,
                                show_rejected=True,
                                max_depth=0)
            s += "\n"


        return s

    def invert(self):
        if self.result == REJECTED:
            return ""
        output = ""
        for child in self.children:
            if isinstance(child, str):
                output += child
            else:
                output += child.invert()
        return output


    def to_string(self, show_position=True, show_result=True,
                  show_rejected=True, depth=0, indentation_space_count=3,
                  max_depth=None):

        indentation = " " * depth * indentation_space_count

        if max_depth is not None and depth > max_depth:
            return ""

        if self.result == REJECTED and show_rejected == False:
            return ""

        if self.parent is not None:
            parent_name = self.parent.name
        else:
            parent_name = "None"

        if self.result == ACCEPTED:
            result_string = GREEN_PREFIX + "ACCEPTED" + RESET_POSTFIX
        elif self.result == REJECTED:
            result_string = RED_PREFIX + "REJECTED" + RESET_POSTFIX
        elif self.result is None:
            result_string = YELLOW_PREFIX + "UNDECIDED" + RESET_POSTFIX
        else:
            result_string = f"UNKNOWN RESULT VALUE: {self.result}"

        if self.cursor_position == EOF_POSITION_MARKER:
            position_string = BOLD_PREFIX + "EOF" + RESET_POSTFIX
        else:
            position_string = f"(row: {self.cursor_position[0]} col: {self.cursor_position[1]})"

        if self.name in EXPRESSION_TYPES:
            name_string = f"{self.name}"
        else:
            name_string = f"{self.name}"

        s = name_string

        if show_result:
            s += " " + result_string

        if show_position:
            s += " " + position_string

        opening = indentation + s

        if len(self.children) == 0:
            opening += "\n"
        elif len(self.children) == 1 and isinstance(self.children[0], str):
            opening += ": "
        else:
            opening += ":\n"

        middle = ""

        if self.children is not None:
            for child in self.children:
                if isinstance(child, str):
                    middle += f"'{escape(child)}'" + "\n"
                else:
                    middle += child.to_string(depth=depth+1,
                                              indentation_space_count=indentation_space_count,
                                              show_rejected=show_rejected,
                                              show_result=show_result,
                                              show_position=show_position,
                                              max_depth=max_depth)

        if depth == 0:
            return (opening + middle).strip()
        else:
            return (opening + middle)

    def drop_history(self):
        if self.result == REJECTED:
            return None
        elif self.name == ASSERT:
            return None
        elif self.name == REJECT:
            return None
        else:
            if len(self.children) == 0:
                return self # an EOL or EOF
            elif isinstance(self.children[0], str):
                return self # self is a terminal
            else:
                new_children = []

                for child in self.children:
                    grandchildren = child.drop_history()
                    if grandchildren is None:
                        continue
                    elif isinstance(grandchildren, list):
                        new_children += grandchildren
                    else:
                        new_children.append(grandchildren)

                if self.name in PRIMITIVE_TYPES:
                    return new_children
                else:
                    self.children = new_children
                    for child in self.children:
                        child.parent = self
                    return self

                return self


    def apply_transforms(self, transforms):

        if len(self.children) == 1 and isinstance(self.children[0], str):
            if self.name in transforms:
                return transforms[self.name](self)
            else:
                return self
        else:
            new_children = []

            for child in self.children:
                if not isinstance(child, str):
                    new_child = child.apply_transforms(transforms)
                    if new_child is not None: 
                        new_children.append(new_child)
                        new_child.parent = self

            self.children = new_children

        if self.name in transforms:
            self = transforms[self.name](self)

        return self
