import re
from xiatl.parsing.pegboard.core.constants import *
from xiatl.parsing.pegboard.core.parse_result import *
from xiatl.parsing.pegboard.core.parse_node import *

# TODO : make use of cache
# TODO : add option for non-error reporting mode (i.e., don't save parse nodes for rejections)
class Parser:

    def __init__(self, start, terminals, non_terminals):

        if not isinstance(start, str):
            raise ValueError(f"start symbol must be specified as a 'str', not amust be specified as a '{type(start)}'")

        if not isinstance(terminals, dict):
            raise ValueError(f"terminals must be a 'dict' with items of the form 'name':'pattern'")

        for terminal, pattern in terminals.items():
            if not isinstance(pattern, str):
                raise ValueError(f"terminal '{terminal}' must have a pattern specified as a 'str' not a '{type(pattern)}'")

        for non_terminal, rule in non_terminals.items():
            if not isinstance(rule, list):
                raise ValueError(f"non-terminal '{non_terminal}' must have a rule specified as a 'list' not a '{type(rule)}'")

        if start not in non_terminals: 
            raise ValueError(f"start symbol: '{start}' is not in the given non-terminals:\n{non_terminals}")

        self.start = start
        self.terminals = terminals
        self.non_terminals = non_terminals

    def enumerate_input_string(self):

        line = 1
        column = 1
        self.position_table = []

        for i, char in enumerate(self.input_string):
            if char == "\n":
                self.position_table.append((line + 0.5, column - 0.5))
                column = 1
                line += 1
            else:
                self.position_table.append((line, column))
                column += 1

        self.position_table.append(EOF_POSITION_MARKER)

    def parse_file(self, filename, drop_history=True):

        with open(filename, "r", encoding="utf-8") as f:
            input_string = f.read()

        return self.parse_string(input_string, drop_history)

    def parse_string(self, input_string, drop_history=True):

        self.cursor_position = 0
        self.input_string = input_string
        self.enumerate_input_string()
        self.expectation_context = EXPECTED
        self.expected_terminals = []
        self.unexpected_terminals = []
        self.max_cursor_position = self.cursor_position
        result, parse_tree = self.evaluate_expression([NON_TERMINAL, self.start])

        if result == ACCEPTED:
            parse_result = Parse_Result(result, parse_tree, None, None, self.input_string,
                                        self.max_cursor_position, self.position_table)
            if drop_history:
                parse_result.drop_history()
            return parse_result

        else:
            return Parse_Result(result, parse_tree, self.expected_terminals, self.unexpected_terminals,
                                self.input_string, self.max_cursor_position,
                                self.position_table)

    def save_expectation(self, new_parse_node, result):

        t = (new_parse_node, self.position_table[self.cursor_position])

        if self.cursor_position > self.max_cursor_position:
            self.max_cursor_position = self.cursor_position
            self.expected_terminals = []
            self.unexpected_terminals = []

        if self.cursor_position == self.max_cursor_position:
            if self.expectation_context == EXPECTED and result == REJECTED:
                self.expected_terminals.append(t)
            elif self.expectation_context == UNEXPECTED and result == ACCEPTED:
                self.unexpected_terminals.append(t)

    def evaluate_anon_terminal(self, pattern):

        regex_result = re.match(pattern, self.input_string[self.cursor_position:])

        if regex_result:
            result = ACCEPTED
            length_of_match = regex_result.end() - regex_result.start()
            children = [regex_result.group()]
        else:
            result = REJECTED
            length_of_match = 0
            children = [pattern]

        new_parse_node = Parse_Node(name=ANON_TERMINAL, cursor_position=self.position_table[self.cursor_position],
                                    raw_cursor_position=self.cursor_position,
                                    result=result, children=children,
                                    parent=None) # caller's responsibility to set parent
        self.save_expectation(new_parse_node, result)
        self.cursor_position += length_of_match

        return result, new_parse_node

    def evaluate_terminal(self, name):

        pattern = self.terminals[name]
        regex_result = re.match(pattern, self.input_string[self.cursor_position:])

        if regex_result:
            result = ACCEPTED
            length_of_match = regex_result.end() - regex_result.start()
            children = [regex_result.group()]
        else:
            result = REJECTED
            length_of_match = 0
            children = [pattern]

        new_parse_node = Parse_Node(name=name, cursor_position=self.position_table[self.cursor_position],
                                    raw_cursor_position=self.cursor_position,
                                    result=result, children=children,
                                    parent=None) # caller's responsibility to set parent
        self.save_expectation(new_parse_node, result)
        self.cursor_position += length_of_match

        return result, new_parse_node

    def evaluate_non_terminal(self, name):

        expression = self.non_terminals[name] # this is always a list
        new_parse_node = Parse_Node(name=name, cursor_position=self.position_table[self.cursor_position],
                                    raw_cursor_position=self.cursor_position,
                                    result=None, children=None,
                                    parent=None) # caller's responsibility to set parent
        result, child_parse_node = self.evaluate_expression(expression)
        child_parse_node.parent = new_parse_node
        new_parse_node.result = result
        new_parse_node.children = [child_parse_node]

        return result, new_parse_node

    def evaluate_reject(self, expression):

        self.expectation_context = not self.expectation_context # <- flip it
        old_cursor_position = self.cursor_position
        new_parse_node = Parse_Node(name=REJECT, cursor_position=self.position_table[self.cursor_position],
                                    raw_cursor_position=self.cursor_position,
                                    result=None, children=None,
                                    parent=None) # caller's responsibility to set parent
        child_result, child_parse_node = self.evaluate_expression(expression)

        if child_result == ACCEPTED: 
            self.cursor_position = old_cursor_position
            result = REJECTED
        else:
            result = ACCEPTED

        child_parse_node.parent = new_parse_node
        new_parse_node.children = [child_parse_node]
        new_parse_node.result = result
        self.expectation_context = not self.expectation_context # <- restore it

        return result, new_parse_node

    def evaluate_assert(self, expression):

        old_cursor_position = self.cursor_position
        new_parse_node = Parse_Node(name=ASSERT, cursor_position=self.position_table[self.cursor_position],
                                    raw_cursor_position=self.cursor_position,
                                    result=None, children=None,
                                    parent=None) # caller's responsibility to set parent
        child_result, child_parse_node = self.evaluate_expression(expression)

        if child_result == ACCEPTED: 
            self.cursor_position = old_cursor_position
            result = ACCEPTED
        else:
            result = REJECTED

        child_parse_node.parent = new_parse_node
        new_parse_node.children = [child_parse_node]
        new_parse_node.result = result

        return result, new_parse_node
            
    def evaluate_at_least_zero(self, expression):

        result = ACCEPTED
        new_parse_node = Parse_Node(name=AT_LEAST_ZERO, cursor_position=self.position_table[self.cursor_position],
                                    raw_cursor_position=self.cursor_position,
                                    result=result, children=None,
                                    parent=None) # caller's responsibility to set parent

        while True:
            child_result, child_parse_node = self.evaluate_expression(expression)
            child_parse_node.parent = new_parse_node
            new_parse_node.children.append(child_parse_node)

            if child_result == REJECTED:
                break
            else:
                pass

        return result, new_parse_node

    def evaluate_at_least_one(self, expression):

        new_parse_node = Parse_Node(name=AT_LEAST_ONE, cursor_position=self.position_table[self.cursor_position],
                                    raw_cursor_position=self.cursor_position,
                                    result=None, children=None,
                                    parent=None) # caller's responsibility to set parent
        required_child_result, required_child_parse_node = self.evaluate_expression(expression)
        required_child_parse_node.parent = new_parse_node
        new_parse_node.children.append(required_child_parse_node)

        if required_child_result == REJECTED:
            result = REJECTED
        else:
            result = ACCEPTED

            while True:
                child_result, child_parse_node = self.evaluate_expression(expression)
                child_parse_node.parent = new_parse_node
                new_parse_node.children.append(child_parse_node)

                if child_result == REJECTED:
                    break
                else:
                    pass

        new_parse_node.result = result

        return result, new_parse_node

    def evaluate_sequence(self, expressions):

        old_cursor_position = self.cursor_position
        new_parse_node = Parse_Node(name=SEQUENCE, cursor_position=self.position_table[self.cursor_position],
                                    raw_cursor_position=self.cursor_position,
                                    result=None, children=None,
                                    parent=None) # caller's responsibility to set parent
        result = ACCEPTED

        for expression in expressions:
            child_result, child_parse_node = self.evaluate_expression(expression)
            child_parse_node.parent = new_parse_node
            new_parse_node.children.append(child_parse_node)

            if child_result == REJECTED:
                self.cursor_position = old_cursor_position
                result = REJECTED
                break
            else:
                pass

        new_parse_node.result = result

        return result, new_parse_node

    def evaluate_choice(self, expressions):

        old_cursor_position = self.cursor_position
        new_parse_node = Parse_Node(name=CHOICE, cursor_position=self.position_table[self.cursor_position],
                                    raw_cursor_position=self.cursor_position,
                                    result=None, children=None,
                                    parent=None) # caller's responsibility to set parent
        result = REJECTED

        for expression in expressions:
            child_result, child_parse_node = self.evaluate_expression(expression)
            child_parse_node.parent = new_parse_node
            new_parse_node.children.append(child_parse_node)

            if child_result == ACCEPTED:
                result = ACCEPTED
                break
            else:
                self.cursor_position = old_cursor_position

        new_parse_node.result = result

        return result, new_parse_node

    def evaluate_optional(self, expression):

        result = ACCEPTED # optional always accepts
        new_parse_node = Parse_Node(name=OPTIONAL, cursor_position=self.position_table[self.cursor_position],
                                    raw_cursor_position=self.cursor_position,
                                    result=result, children=None,
                                    parent=None) # caller's responsibility to set parent
        child_result, child_parse_node = self.evaluate_expression(expression)
        child_parse_node.parent = new_parse_node
        new_parse_node.children = [child_parse_node]

        return result, new_parse_node

    def evaluate_eof(self):

        if self.cursor_position == len(self.input_string):
            result = ACCEPTED
        else:
            result = REJECTED

        new_parse_node = Parse_Node(name=EOF, cursor_position=self.position_table[self.cursor_position],
                                    raw_cursor_position=self.cursor_position,
                                    result=result, children=None,
                                    parent=None) # caller's responsibility to set parent
        self.save_expectation(new_parse_node, result)

        return result, new_parse_node

    def evaluate_eol(self):

        pattern = r"\r\n|[\r\n\u0085\u2028\u2029]"
        regex_result = re.match(pattern, self.input_string[self.cursor_position:])

        if regex_result:
            result = ACCEPTED
            length_of_match = regex_result.end() - regex_result.start()
            children = [regex_result.group()]
        else:
            result = REJECTED
            length_of_match = 0
            children = None

        new_parse_node = Parse_Node(name=EOL, cursor_position=self.position_table[self.cursor_position],
                                    raw_cursor_position=self.cursor_position,
                                    result=result, children=children,
                                    parent=None) # caller's responsibility to set parent
        self.save_expectation(new_parse_node, result)

        self.cursor_position += length_of_match

        return result, new_parse_node

    def evaluate_expression(self, expression): 

        assert isinstance(expression, list)
        expression_type = expression[0]
        expression_items = expression[1:]

        if expression_type == SEQUENCE:
            result, child_parse_node = self.evaluate_sequence(expression_items)
        elif expression_type == CHOICE:
            result, child_parse_node = self.evaluate_choice(expression_items)
        elif expression_type == AT_LEAST_ZERO:
            assert len(expression_items) == 1 # AT_LEAST_ZERO can only be evaluated on one expression
            expression = expression_items[0]
            result, child_parse_node = self.evaluate_at_least_zero(expression)
        elif expression_type == AT_LEAST_ONE:
            assert len(expression_items) == 1 # AT_LEAST_ONE can only be evaluated on one expression
            expression = expression_items[0]
            result, child_parse_node = self.evaluate_at_least_one(expression)
        elif expression_type == OPTIONAL:
            assert len(expression_items) == 1 # OPTIONAL can only be evaluated on one expression
            expression = expression_items[0]
            result, child_parse_node = self.evaluate_optional(expression)
        elif expression_type == NON_TERMINAL:
            child_name = expression_items[0]
            result, child_parse_node = self.evaluate_non_terminal(child_name)
        elif expression_type == ANON_TERMINAL:
            child_pattern = expression_items[0]
            result, child_parse_node = self.evaluate_anon_terminal(child_pattern)
        elif expression_type == TERMINAL:
            child_name = expression_items[0]
            result, child_parse_node = self.evaluate_terminal(child_name)
        elif expression_type == REJECT:
            assert len(expression_items) == 1 # REJECT can only be evaluated on one expression
            expression = expression_items[0]
            result, child_parse_node = self.evaluate_reject(expression)
        elif expression_type == ASSERT:
            assert len(expression_items) == 1 # ASSERT can only be evaluated on one expression
            expression = expression_items[0]
            result, child_parse_node = self.evaluate_assert(expression)
        elif expression_type == EOL:
            assert len(expression_items) == 0 # EOL has no items
            result, child_parse_node = self.evaluate_eol()
        elif expression_type == EOF:
            assert len(expression_items) == 0 # EOF has no items
            result, child_parse_node = self.evaluate_eof()
        else:
            raise ValueError(f"unknown expression_type '{expression_type}'")

        return result, child_parse_node
