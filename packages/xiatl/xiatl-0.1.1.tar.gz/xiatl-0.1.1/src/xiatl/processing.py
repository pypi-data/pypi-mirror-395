from xiatl.parsing import parse_string
from xiatl.parsing.utilities import is_terminal, verify_initial_ast
from xiatl.utilities import ensure, Internal_Error
from xiatl.constants import PROJECT_ROOT, LOCAL_ROOT, PARENT_NODE
from xiatl.node import Node
from xiatl.node_reference import Node_Reference
from xiatl.errors import *

def process_string(input_string, name, error_message):

    parse_tree = parse_string(input_string)

    if not parse_tree.accepted:
        raise Processing_Error(
        message = error_message,
        report = parse_tree.generate_report()
        )
    else:
        ast = parse_tree.parse_tree
        result = process_input(ast, name=name)

    return result

def process_input(ast, name=None):

    verify_initial_ast(ast)
    scope_result = process_scope(ast.children[0])
    local_root = Node(node_type=LOCAL_ROOT, name=name, children=scope_result)
    return local_root

def finalize_project_tree(node, project_root):

    if isinstance(node, Node):
        for child in node.children:
            if not isinstance(child, str):
                child.parent = node
                finalize_project_tree(child, project_root)
    elif isinstance(node, Node_Reference):
        reference = node
        if reference.components[0] == PROJECT_ROOT:
            reference.item = resolve_reference(reference.components[1:], project_root)
        else:
            Internal_Error(f"Unresolved non-project-based reference found with start: '{reference.components[0]}'")
    else:
        raise Internal_Error(f"Unknown node type for '{node}'")

def finalize_local_tree(node, local_root):

    if isinstance(node, Node):
        for child in node.children:
            if not isinstance(child, str):
                child.parent = node
                finalize_local_tree(child, local_root)
    elif isinstance(node, Node_Reference):
        reference = node
        if reference.components[0] == PARENT_NODE:
            if reference.parent is None:
                raise Processing_Error("Reference path cannot escape local root, remove reference or use a project-based path.")
            reference.item = resolve_reference(reference.components[1:], reference.parent.parent)
        elif reference.components[0] == LOCAL_ROOT:
            reference.item = resolve_reference(reference.components[1:], local_root)
        elif reference.components[0] == PROJECT_ROOT:
            pass # these will be resolved at project-level later
        else:
            reference.item = resolve_reference(reference.components, reference.parent)
    else:
        raise Internal_Error(f"Unknown node type for '{node}'")

def resolve_reference(reference_components, root):

    if len(reference_components) == 0:
        return root

    if isinstance(reference_components[0], str):
        name = reference_components[0]
        new_root = None
        for child in root.children:
            if (not (isinstance(child, str) or isinstance(child, Node_Reference))) and child.name == name:
                new_root = child
        if new_root is not None:
            return resolve_reference(reference_components[1:], new_root)
        else:
            raise Processing_Error(f"Invalid reference name '{name}'")
    else:
        index = reference_components[0]
        if 0 <= index < len(root.children):
            child = root.children[index]
            if isinstance(child, Node_Reference):
                raise Processing_Error(f"Encountered illegal reference to reference.")
            new_root = child
            return resolve_reference(reference_components[1:], new_root)
        else:
            raise Processing_Error(f"Invalid reference index '{index}'")

def process_scope(ast):

    ensure(ast.name == "scope")
    resulting_nodes = []

    for child in ast.children:
        ensure(child.name == "item")
        ensure(len(child.children) == 1)
        grandchild = child.children[0]
        n = grandchild.name

        if n == "WHITESPACE":
            p = process_WHITESPACE
        elif n == "verbatim":
            p = process_verbatim
        elif n == "comment":
            p = process_comment
        elif n == "node":
            p = process_node
        elif n == "LITERAL":
            p = process_LITERAL
        elif n == "reference":
            p = process_reference
        else:
            raise Internal_Error(f"unknown item type '{n}'")

        resulting_node = p(grandchild)

        if not (resulting_node is None):
            ensure(isinstance(resulting_node, Node) or isinstance(resulting_node, str) or isinstance(resulting_node, Node_Reference))

            resulting_nodes.append(resulting_node)
        else:
            pass # we throw it away (was WHITESPACE)

    return resulting_nodes

def process_node(ast):

    node_type = None
    node_name = None
    node_tags = []

    for child in ast.children:
        if child.name == "NODE_TYPE":
            ensure(node_type is None)
            ensure(is_terminal(child))
            node_type = child.children[0]
        elif child.name == "NODE_NAME":
            ensure(node_name is None)
            ensure(is_terminal(child))
            node_name = child.children[0]
        elif child.name == "NODE_TAG":
            ensure(is_terminal(child))
            node_tags.append(child.children[0])
        elif child.name == "scope":
            node_children = process_scope(child)

    return Node(node_type=node_type, name=node_name, tags=node_tags, children=node_children)

def process_verbatim(ast):
    ensure(ast.children[0].name == "VERBATIM_DELIMITER")
    ensure(ast.children[-1].name == "VERBATIM_DELIMITER")
    ensure(ast.children[1].name == "LITERAL")
    ensure(is_terminal(ast.children[1]))
    return ast.children[1].children[0]

def process_LITERAL(ast):
    ensure(is_terminal(ast))
    return ast.children[0]

def process_WHITESPACE(ast):
    return None

def process_comment(ast):
    return None

def process_reference(ast):
    reference_components = []
    ensure(ast.children[0].name == "REFERENCE_DELIMITER")
    for child in ast.children[1:]:
        if child.name == "INDEX":
            reference_components.append(int(child.children[0]))
        elif child.name == "NODE_NAME":
            reference_components.append(child.children[0])
        elif child.name == "special_ref":
            ensure(len(child.children) == 1)
            grandchild = child.children[0]
            if grandchild.name == "PROJECT_ROOT":
                reference_components.append(PROJECT_ROOT)
            elif grandchild.name == "LOCAL_ROOT":
                reference_components.append(LOCAL_ROOT)
            elif grandchild.name == "PARENT_NODE":
                reference_components.append(PARENT_NODE)

    return Node_Reference(reference_components)

    

