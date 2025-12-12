from xiatl.parsing.pegboard.core.parser import *
from xiatl.parsing.pegboard.core.constants import *
from xiatl.parsing.pegboard.syntax.grammar import *
from xiatl.parsing.pegboard.syntax.transforms import *

class GrammarParseError(Exception):
    def __init__(self, message, report):
        super().__init__(message)
        self.message = message
        self.report = report
    def __str__(self):
        return self.message + "\n" + self.report
        

def generate_parser(start_symbol, grammar_string=None, grammar_filename=None):
    syntax_parser = Parser(start="Grammar",
                           terminals=syntax_terminals,
                           non_terminals=syntax_non_terminals)

    if grammar_string is not None and grammar_filename is None:
        grammar_result = syntax_parser.parse_string(grammar_string)
    elif grammar_filename is not None and grammar_string is None:
        with open(grammar_filename, "r") as f:
            grammar_string = f.read()
        grammar_result = syntax_parser.parse_string(grammar_string)
    else:
        raise ValueError("provide one (and only one) of grammar_string, grammar_filename")

    if grammar_result.accepted:
        grammar_result.apply_transforms(syntax_transforms)
    else:
        raise GrammarParseError(
                message = "Invalid grammar string",
                report = grammar_result.generate_report()
                )

    def transform(node):
        if isinstance(node, str):
            return node
        elif node.name == "Identifier":
            identifier = node.children[0]
            if identifier.isupper():
                return [TERMINAL, identifier]
            else:
                return [NON_TERMINAL, identifier]
        elif node.name == "Pattern":
            assert isinstance(node.children[0], str)
            return [ANON_TERMINAL, node.children[0]]
        elif node.name == "EOF":
            return [EOF]
        elif node.name == "EOL":
            return [EOL]
        elif node.name == "Reject":
            assert len(node.children) == 1 # Reject should only have one child
            return [REJECT, transform(node.children[0])]
        elif node.name == "Assert":
            assert len(node.children) == 1 # Assert should only have one child
            return [ASSERT, transform(node.children[0])]
        elif node.name == "AtLeastZero":
            assert len(node.children) == 1 # AtLeastZero should only have one child
            return [AT_LEAST_ZERO, transform(node.children[0])]
        elif node.name == "AtLeastOne":
            assert len(node.children) == 1 # AtLeastOne should only have one child
            return [AT_LEAST_ONE, transform(node.children[0])]
        elif node.name == "Optional":
            assert len(node.children) == 1 # Optional should only have one child
            return [OPTIONAL, transform(node.children[0])]
        elif node.name == "Sequence":
            items = []
            for child in node.children:
                items.append(transform(child))
            return [SEQUENCE] + items
        elif node.name == "Choice":
            items = []
            for child in node.children:
                items.append(transform(child))
            return [CHOICE] + items
        else:
            raise RuntimeError(f"unknown node type {node.name} (this is a bug in parser, please report to maintainers)")

    def verify(node, identifiers):
        if isinstance(node, str):
            return
        elif node.name == "Identifier":
            identifier = node.children[0]
            if identifier not in identifiers:
                raise GrammarParseError(
                        message = f"Identifier '{identifier}' is undefined in grammar string",
                        report = grammar_result.generate_input_snippet(cursor_position=node.raw_cursor_position)
                        )
        else:
            for child in node.children:
                verify(child, identifiers)

    terminals = dict()
    non_terminals = dict()
    grammar_ast = grammar_result.parse_tree
    identifiers = dict()

    for definition_ast in grammar_ast.children:
        if definition_ast.name == "Definition":
            identifier_ast = definition_ast.children[0]
            identifier = identifier_ast.children[0]
            rule_ast = definition_ast.children[1]
            identifiers[identifier] = (rule_ast, identifier_ast)

    for identifier, (rule_ast, identifier_ast) in identifiers.items():
        verify(rule_ast, identifiers)
        if identifier.islower():
            non_terminals[identifier] = (rule_ast, identifier_ast)
        elif identifier.isupper():
            terminals[identifier] = (rule_ast, identifier_ast)
        else:
            raise GrammarParseError(
                    message = f"Identifier '{identifier}' must be either all upper case (a terminal) or all lower case (a non-terminal)",
                    report = grammar_result.generate_input_snippet(cursor_position=identifier_ast.raw_cursor_position)
                    )

    for terminal, (rule_ast, identifier_ast) in terminals.items():
        if not rule_ast.name == "Pattern":
            raise GrammarParseError(
                    message = f"Definition of terminal '{identifier_ast.children[0]}' must contain a single pattern",
                    report = grammar_result.generate_input_snippet(cursor_position=identifier_ast.raw_cursor_position)
                    )
        assert len(rule_ast.children) == 1
        pattern = rule_ast.children[0]
        terminals[terminal] = pattern
    for non_terminal, (rule_ast, identifier_ast) in non_terminals.items():
        non_terminals[non_terminal] = transform(rule_ast)

    parser = Parser(start=start_symbol,
                    terminals=terminals,
                    non_terminals=non_terminals)

    return parser

