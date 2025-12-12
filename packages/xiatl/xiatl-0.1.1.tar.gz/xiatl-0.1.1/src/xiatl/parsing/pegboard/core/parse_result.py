import math
from xiatl.parsing.pegboard.core.constants import *
from xiatl.parsing.pegboard.core.utilities import *

class Parse_Result:

    def __init__(self, accepted, parse_tree, expected_terminals, unexpected_terminals,
                 input_string, max_cursor_position, position_table):

        self.accepted = accepted
        self.parse_tree = parse_tree
        self.expected_terminals = expected_terminals
        self.unexpected_terminals = unexpected_terminals
        self.input_string = input_string
        self.max_cursor_position = max_cursor_position
        self.position_table = position_table

    def invert(self):

        return self.parse_tree.invert()

    def drop_history(self):

        self.parse_tree.drop_history()

    def _generate_input_snippet(self, cursor_position=None, input_snippet_size=80):

        if cursor_position is None:
            cursor_position = self.max_cursor_position
        working_string = self.input_string + EOF_MARKER
        min_index = 0
        max_index = len(working_string) - 1
        character_count_left = math.ceil((input_snippet_size-1)/2)
        character_count_right = math.floor((input_snippet_size-1)/2)
        lower_bound = max(cursor_position - character_count_left, min_index)
        upper_bound = min(cursor_position + character_count_right, max_index)
        if lower_bound == cursor_position:
            input_snippet_left = ""
        else:
            input_snippet_left = escape(working_string[lower_bound:cursor_position])
        if upper_bound == cursor_position:
            input_snippet_right = ""
        else:
            input_snippet_right = escape(working_string[cursor_position+1:upper_bound+1])
        input_snippet_center = escape(working_string[cursor_position])
        if lower_bound != min_index:
            input_snippet_left = "... " + input_snippet_left
        if upper_bound != max_index:
            input_snippet_right = input_snippet_right + " ..."
        if len(input_snippet_center) > 1:
            pointer = "^" + " " * (len(input_snippet_center) - 1)
        else:
            pointer = "^"
        input_snippet = input_snippet_left + input_snippet_center + input_snippet_right
        marker_line = " " * len(input_snippet_left) + pointer + " " * len(input_snippet_right)
        return input_snippet, marker_line

    def generate_input_snippet(self, cursor_position=None, color_prefix=RED_PREFIX, indentation_space_count=3):

        if cursor_position is None:
            cursor_position = self.max_cursor_position

        s = color_prefix + "\n"
        position_tuple = self.position_table[cursor_position]
        s += f"(row: {position_tuple[0]} col: {position_tuple[1]}):" + "\n"
        input_snippet, marker_line = self._generate_input_snippet(cursor_position)
        input_snippet = indentation_space_count * " " + input_snippet
        marker_line = indentation_space_count * " " + marker_line
        s += input_snippet + "\n"
        s += marker_line + "\n"
        s += RESET_POSTFIX

        return s

    def generate_report(self):

        s = self.generate_input_snippet()
        s += RED_PREFIX + "\n"

        if len(self.expected_terminals) > 0:
            s += "EXPECTED ONE OF:\n"
            for terminal, position in self.expected_terminals:
                s += terminal.to_string(show_result=False, show_position=False, depth=1)

        if len(self.unexpected_terminals) > 0:
            s += "DID NOT EXPECT:\n"
            for terminal, position in self.unexpected_terminals:
                s += terminal.to_string(show_result=False, show_position=False, depth=1)

        s += RESET_POSTFIX

        return s

    def __repr__(self): 


        if self.accepted:
            s = "INPUT ACCEPTED"
            lines = "\n" + len(s) * "-" + "\n"
            s = lines + s + lines
            s += self.parse_tree.to_string(show_position=False, show_result=False, show_rejected=False)
        else:
            s = f"INPUT NOT ACCEPTED"
            lines = "\n" + len(s) * "-" + "\n"
            s = lines + s + lines
            # s += self.parse_tree.to_string()

            s += self.generate_report()
        return s

    def apply_transforms(self, transforms):
        self.parse_tree.apply_transforms(transforms)
