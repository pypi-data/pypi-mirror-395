from textwrap import dedent
from copy import deepcopy
from xiatl.parsing import parse_string
from xiatl.parsing.utilities import is_terminal, verify_initial_ast
from xiatl.utilities import ensure, Internal_Error
from xiatl.constants import RED_PREFIX, GREEN_PREFIX, RESET_POSTFIX, NAME, VALUE, VALIDATOR
from xiatl.macro_signature import *
from xiatl.parsing.pegboard.core.parse_node import Parse_Node, generate_dummy_node
from xiatl.errors import *

def resolve_file(filename, max_iterations=None, debug=False):

    if not isinstance(debug, bool):
        raise ValueError("debug must be of type 'bool'")

    if not isinstance(filename, str):
        raise ValueError("filename must be of type 'str'")

    with open(filename, "r", encoding="utf-8") as f:
        input_string = f.read()

    return _resolve_string(input_string=input_string, max_iterations=max_iterations, error_message="Invalid input file", debug=debug)

def resolve_string(input_string, max_iterations=None, debug=False):
    
    return _resolve_string(input_string, max_iterations=max_iterations, debug=debug, error_message="Invalid input string")

def _resolve_string(input_string, max_iterations=None, debug=None, error_message="Invalid input string"):

    target_string = input_string
    i = 0
    while True:
        if (max_iterations is not None) and (i == max_iterations):
            return target_string
        parse_tree = parse_string(target_string)

        if not parse_tree.accepted:
            raise Resolution_Error(
            message = error_message,
            report = parse_tree.generate_report()
            )
        else:
            r = Resolver(parse_tree, debug)
            r.resolve_input()

        result = parse_tree.invert()
        if target_string == result:
            return result
        else:
            target_string = result
        i+=1

class Resolution_Scope:

    def __init__(self, scope_ast, parent_scope=None):
        self.scope_ast = scope_ast
        if parent_scope is None:
            self.macro_signatures = []
            self.macro_bodies = []
            self.macro_asts = []
        else:
            self.macro_signatures = deepcopy(parent_scope.macro_signatures)
            self.macro_bodies = deepcopy(parent_scope.macro_bodies)
            self.macro_asts = deepcopy(parent_scope.macro_asts)


    def add_macro_definition(self, new_macro_signature, new_body, new_ast):

        replaced_existing = False
        for i, existing_signature in enumerate(self.macro_signatures):
            if existing_signature.basic_signature == new_macro_signature.basic_signature:
                self.macro_signatures[i] = new_macro_signature
                self.macro_bodies[i] = new_body
                self.macro_asts[i] = new_ast
                replaced_existing = True
                break

        if not replaced_existing:
            self.macro_signatures.append(new_macro_signature)
            self.macro_bodies.append(new_body)
            self.macro_asts.append(new_ast)

class Resolver:

    def __init__(self, parse_result, debug):

        self.debug = debug
        self.parse_result = parse_result

        ast = self.parse_result.parse_tree
        verify_initial_ast(ast)
        self.current_scope = Resolution_Scope(ast.children[0], parent_scope=None)

        self.python_insertion_buffer = []
        def insert(*values, end=" "):
            for value in values:
                self.python_insertion_buffer.append(str(value)+end)

        self.macro_arguments_stack = []

        def argument(name):
            current_arguments = self.macro_arguments_stack[-1]
            if name in current_arguments:
                from xiatl import load_string
                node = load_string(current_arguments[name].value)
                return node.children
            else:
                raise RuntimeError(f"argument '{name}' does not exist")

        def my_breakpoint():
            input(f"{RED_PREFIX}You appear to be trying to debug Python code in XIATL.\nThis feature is still under development!\nPress Enter to continue normal execution...{RESET_POSTFIX}")

        self.python_globals = { "insert" : insert , "breakpoint" : my_breakpoint, "argument" : argument} 
        self.locals_stack = [self.python_globals]

    def print_step(self, do_print, message="", show_numbers=True):

        if self.debug and do_print:
            lines = self.current_scope.scope_ast.invert().split("\n")

            if len(lines) == 1 and lines[0] == "":
                print(" [NOTHING TO INSERT]")
            elif show_numbers:
                digits = len(str(len(lines)+1))
                for i, line in enumerate(lines):
                    print(f" {i+1:{digits}} "+line)
            else:
                for i, line in enumerate(lines):
                    print(f" "+line)

            while True:
                if message != "":
                    print(f" [debug message]: {message}")

                input_message = " Enter 's' to step, 'c' to continue, 'd' to view current defs: "
                user_input = input(input_message).strip()
                print(" " + (len(input_message)) * "-")

                if user_input == "s":
                    break
                elif user_input == "c":
                    self.debug = False
                    break
                elif user_input == "d":
                    if len(self.current_scope.macro_asts) == 0:
                        print(" [NO DEFINITIONS IN CURRENT SCOPE]")
                    print(GREEN_PREFIX, end="")
                    for macro_ast in self.current_scope.macro_asts:
                        print(macro_ast.invert().strip())
                        print()
                    print(RESET_POSTFIX, end="")
                    print(f" [debug message]: all macro definitions printed")
                elif user_input == "":
                    print(" [debug message]: please enter a command")
                else:
                    print(f" [debug message]: unknown command: '{user_input}'")

    def generate_input_snippet(self, cursor_position):

        return self.parse_result.generate_input_snippet(cursor_position=cursor_position)

    def resolve_input(self):

        self.resolve_scope(self.current_scope.scope_ast)
        self.print_step(do_print=True, message="resolution complete")

    def resolve_scope(self, ast):

        ensure(ast.name == "scope")

        previous_scope = self.current_scope
        self.current_scope = Resolution_Scope(ast, parent_scope=self.current_scope)

        resolved_children = []
        unresolved_children = ast.children
        modified = False

        while len(unresolved_children) > 0:
            child = unresolved_children.pop(0)
            ensure(child.name == "item")
            ensure(len(child.children) == 1)
            grandchild = child.children[0]
            n = grandchild.name

            if n == "macro":
                r = self.resolve_macro
                modified = True
                message = "macro resolved"
            elif n == "block_python":
                r = self.resolve_block_python
                modified = True
                message = "block python executed"
            elif n == "inline_python":
                r = self.resolve_inline_python
                modified = True
                message = "inline python executed"
            elif n == "breakpoint":
                r = self.resolve_breakpoint
                modified = True
                message = "hit breakpoint"
            elif n == "node":
                r = self.resolve_node
                modified = True
                message = "node resolved"
            else:
                r = self.nop
                modified = False
                message = ""

            result = r(grandchild) # a parse node

            if isinstance(result, Parse_Node):
                resolved_children.append(result)
            else:
                Internal_Error(f"Unknown result type for '{result}'")

            ast.children = resolved_children + unresolved_children
            self.print_step(do_print=modified, message=message)

        self.current_scope = previous_scope

    def flush_python_insertion_buffer(self):

        new_parse_nodes = []

        for literal in self.python_insertion_buffer:
            new_parse_node = generate_dummy_node(name="LITERAL", children=[literal])
            new_parse_nodes.append(new_parse_node)

        self.python_insertion_buffer = []
        new_node = generate_dummy_node(name="wrapper", children=new_parse_nodes)

        return new_node

    def resolve_block_python(self, ast):

        ensure(len(ast.children) == 3)
        ensure(ast.children[0].name == "BLOCK_DELIMITER")
        ensure(ast.children[1].name == "PYTHON_CODE")
        ensure(ast.children[2].name == "BLOCK_DELIMITER")
        ensure(is_terminal(ast.children[1]))
        code = dedent(ast.children[1].children[0])

        old_scope = self.current_scope
        self.current_scope = Resolution_Scope(ast, parent_scope=old_scope)
        self.print_step(do_print=True, message="executing block python", show_numbers=False)

        try:
            exec(code, locals=self.locals_stack[-1], globals=self.python_globals)
        except Exception as e:
            raise Execution_Error(
                    message="Error executing block python",
                    report=self.generate_input_snippet(cursor_position=ast.raw_cursor_position),
                    code = code,
                    code_message = str(e)
                    ) from e
        
        new_parse_node = self.flush_python_insertion_buffer()
        self.current_scope = Resolution_Scope(new_parse_node)
        self.print_step(do_print=True, message="block python result", show_numbers=False)
        self.current_scope = old_scope

        return new_parse_node

    def resolve_inline_python(self, ast):

        ensure(len(ast.children) == 1)

        if ast.children[0].name == "inline_access":
            access_ast = ast.children[0]
            ensure(len(access_ast.children) == 2)
            ensure(access_ast.children[1].name == "LITERAL")
            var_name = access_ast.children[1].children[0]
            code = f"insert({var_name}, end='')"
        elif ast.children[0].name == "inline_call":
            call_ast = generate_dummy_node(children=ast.children[0].children[1:])
            code = f"insert({call_ast.invert()}, end='')"
        else:
            Internal_Error(f"Unknown type for inline python {self.children[0].name}")

        old_scope = self.current_scope
        self.current_scope = Resolution_Scope(ast, parent_scope=self.current_scope)
        self.print_step(do_print=True, message="executing inline python", show_numbers=False)

        try:
            exec(code, locals=self.locals_stack[-1], globals=self.python_globals)
        except Exception as e:
            raise Execution_Error(
                    message="Error executing inline python",
                    report=self.generate_input_snippet(cursor_position=ast.raw_cursor_position),
                    code = code,
                    code_message = str(e)
                    ) from e

        new_parse_node = self.flush_python_insertion_buffer()
        self.current_scope = Resolution_Scope(new_parse_node)
        self.print_step(do_print=True, message="inline python result", show_numbers=False)
        self.current_scope = old_scope

        return new_parse_node

    def resolve_macro(self, ast):

        ensure(len(ast.children) == 1)
        ast = ast.children[0]

        if ast.name == "macro_call":
            return self.resolve_macro_call(ast)
        elif ast.name == "macro_definition":
            return self.resolve_macro_definition(ast)
        else:
            raise Internal_Error(f"unknown macro type '{ast.name}'")

    def resolve_macro_call(self, ast):

        ensure(len(ast.children) == 1)
        ast = ast.children[0]

        if ast.name == "short_call":
            return self.resolve_short_call(ast)
        elif ast.name == "long_call":
            return self.resolve_long_call(ast)
        else:
            raise Internal_Error(f"unknown macro call type '{ast.name}'")

    def resolve_short_call(self, ast):

        old_scope = self.current_scope
        self.current_scope = Resolution_Scope(ast, parent_scope=old_scope)
        self.print_step(do_print=True, message="expanding short macro call", show_numbers=False)

        ensure(len(ast.children) == 2)
        ensure(ast.children[1].name == "LITERAL")
        signature = [ast.children[1].children[0]]

        new_node = self.expand_call(signature, old_scope)
        middle_scope = self.current_scope
        self.current_scope = Resolution_Scope(new_node)
        self.print_step(do_print=True, message="short macro call result", show_numbers=False)
        self.current_scope = middle_scope

        self.current_scope = old_scope

        return new_node

    def resolve_long_call(self, ast):

        old_scope = self.current_scope
        self.current_scope = Resolution_Scope(ast, parent_scope=old_scope)
        self.print_step(do_print=True, message="expanding long macro call", show_numbers=False)

        signature = []
        for child in ast.children:
            if child.name == "call_item":
                ensure(len(child.children) == 1)
                grandchild = child.children[0]
                if grandchild.name == "argument_list":
                    signature.append(self.resolve_argument_list(grandchild, is_call=True))
                elif grandchild.name == "LITERAL":
                    ensure(len(grandchild.children) == 1)
                    ensure(isinstance(grandchild.children[0], str))
                    signature.append(grandchild.children[0])
                else:
                    raise Internal_Error(f"unknown type for definition item {grandchild.name}")
            else:
                pass # ignore everything else

        new_node = self.expand_call(signature, old_scope)
        middle_scope = self.current_scope
        self.current_scope = Resolution_Scope(new_node)
        self.print_step(do_print=True, message="long macro call result", show_numbers=False)
        self.current_scope = middle_scope

        self.current_scope = old_scope

        return new_node

    def expand_call(self, signature, scope_to_search_from):

        call_signature = Macro_Signature(signature)
        found_match = None
        for i, existing_signature in enumerate(scope_to_search_from.macro_signatures):
            resolved_signature = existing_signature.assign(call_signature)
            if resolved_signature is not None:
                found_match = i
                break

        if found_match is None:
            raise Expansion_Error(
                    message="No matching macro signature exists",
                    report=self.generate_input_snippet(cursor_position=self.current_scope.scope_ast.raw_cursor_position)
                    )
        
        self.macro_arguments_stack.append(resolved_signature.argument_dict)
        macro_body = deepcopy(scope_to_search_from.macro_bodies[found_match])
        self.resolve_argument_references(macro_body, resolved_signature)
        self.resolve_scope(macro_body)
        self.macro_arguments_stack.pop()
        return generate_dummy_node(name="wrapper", children=[macro_body.invert().strip()])


    def resolve_argument_references(self, ast, resolved_signature):

        for i in range(len(ast.children)):
            child = ast.children[i]
            if isinstance(child, str):
                continue
            elif child.name == "argument_reference":
                ensure(child.children[2].name == "scope") 
                argument_name = child.children[2]
                self.resolve_scope(argument_name)
                argument_name = argument_name.invert().strip()
                if argument_name not in resolved_signature.argument_dict:
                    raise Expansion_Error(
                            message=f"Invalid argument reference, argument with name '{argument_name}' does not exist in {resolved_signature.argument_dict}",
                            report=self.generate_input_snippet(cursor_position=self.current_scope.scope_ast.raw_cursor_position)
                            )
                else:
                    value_to_substitute = resolved_signature.argument_dict[argument_name].value
                    ensure(isinstance(value_to_substitute, str))
                    ast.children[i] = generate_dummy_node(name="wrapper", children=[value_to_substitute])
            else:
                self.resolve_argument_references(child, resolved_signature)

    def resolve_macro_definition(self, ast):

        ensure(len(ast.children) == 1)
        ast = ast.children[0]

        if ast.name == "standard_definition":
            self.resolve_standard_definition(ast)
        elif ast.name == "python_definition":
            self.resolve_python_definition(ast)
        else:
            raise Internal_Error(f"unknown macro definition type '{ast.name}'")

        return [] # the definition literals get thrown away

    def resolve_standard_definition(self, ast):

        old_scope = self.current_scope
        self.current_scope = Resolution_Scope(ast, parent_scope=old_scope)
        self.print_step(do_print=True, message="resolving standard macro definition", show_numbers=False)

        signature = [] 
        body = None
        for child in ast.children:
            if child.name == "definition_item":
                ensure(len(child.children) == 1)
                grandchild = child.children[0]
                if grandchild.name == "argument_list":
                    signature.append(self.resolve_argument_list(grandchild))
                elif grandchild.name == "LITERAL":
                    ensure(len(grandchild.children) == 1)
                    ensure(isinstance(grandchild.children[0], str))
                    signature.append(grandchild.children[0])
                else:
                    raise Internal_Error(f"unknown type for definition item {grandchild.name}")
            elif child.name == "scope": 
                body = child
            else:
                pass # ignore everything else

        self.print_step(do_print=True, message="standard macro definition resolved", show_numbers=False)
        self.current_scope = old_scope
        # IT IS CRITICAL THAT THE SCOPE IS RESTORED BEFORE WE ADD THE MACRO DEFINITION
        self.current_scope.add_macro_definition(Macro_Signature(signature), body, ast)

    def resolve_python_definition(self, ast):

        old_scope = self.current_scope
        self.current_scope = Resolution_Scope(ast, parent_scope=old_scope)
        self.print_step(do_print=True, message="resolving Python macro definition", show_numbers=False)

        signature = []
        body = None
        for child in ast.children:
            if child.name == "definition_item":
                ensure(len(child.children) == 1)
                grandchild = child.children[0]
                if grandchild.name == "argument_list":
                    signature.append(self.resolve_argument_list(grandchild))
                elif grandchild.name == "LITERAL":
                    ensure(len(grandchild.children) == 1)
                    ensure(isinstance(grandchild.children[0], str))
                    signature.append(grandchild.children[0])
                else:
                    raise Internal_Error(f"unknown type for definition item {grandchild.name}")
            elif child.name == "PYTHON_CODE": 
                body = child
            else:
                pass # ignore everything else

        self.print_step(do_print=True, message="Python macro definition resolved", show_numbers=False)
        self.current_scope = old_scope
        # IT IS CRITICAL THAT THE SCOPE IS RESTORED BEFORE WE ADD THE MACRO DEFINITION
        self.current_scope.add_macro_definition(Macro_Signature(signature), body, ast)

    def resolve_argument_list(self, ast, is_call=False):

        argument_list = []

        old_scope = self.current_scope
        self.current_scope = Resolution_Scope(ast, parent_scope=old_scope)
        self.print_step(do_print=True, message="resolving argument list", show_numbers=False)

        keyword_args_started = False
        
        for child in ast.children:
            if child.name == "argument":
                new_argument = self.resolve_argument(child, is_call)
                if new_argument.value is None and keyword_args_started:
                    raise Expansion_Error(
                            message="Positional argument cannot appear after keyword argument",
                            report=self.generate_input_snippet(cursor_position=self.current_scope.scope_ast.raw_cursor_position)
                            )
                elif new_argument.value is not None:
                    keyword_args_started = True

                if is_call and new_argument.value is None:
                    pass
                else:
                    argument_list.append(new_argument)
            else:
                pass # ignore everything else

        self.print_step(do_print=True, message="argument list resolved", show_numbers=False)
        self.current_scope = old_scope

        return Argument_List(argument_list)

    def resolve_argument(self, ast, is_call=False):

        argument_name=None
        argument_value=None

        old_scope = self.current_scope
        self.current_scope = Resolution_Scope(ast, parent_scope=old_scope)
        self.print_step(do_print=True, message="resolving argument", show_numbers=False)

        for child in ast.children:
            if child.name == "argument_name":
                ensure(len(child.children) == 1)
                grandchild = child.children[0]
                ensure(grandchild.name == "scope")
                self.resolve_scope(grandchild)
                argument_name = grandchild.invert().strip()
            elif child.name == "argument_value":
                ensure(len(child.children) == 1)
                grandchild = child.children[0]
                ensure(grandchild.name == "scope")
                self.resolve_scope(grandchild)
                argument_value = grandchild.invert().strip()
            else:
                pass # ignore everything else

        self.print_step(do_print=True, message="argument resolved", show_numbers=False)
        self.current_scope = old_scope

        if argument_value == "":
            argument_value = None
        if argument_name == "":
            argument_name = None
        
        if not is_call: # this is a bad patch for a quirk of the grammar. Must rewrite later.
            if argument_name is None:
                argument_name = argument_value
                argument_value = None

        return Argument(name=argument_name, value=argument_value)

    def resolve_node(self, ast):

        for child in ast.children:
            if child.name == "scope":
                self.locals_stack.append({})
                self.resolve_scope(child)
                self.locals_stack.pop()

        return ast

    def resolve_breakpoint(self, ast):
        self.debug = True
        return [] # throw away the breakpoint literals

    def nop(self, ast):
        return ast

