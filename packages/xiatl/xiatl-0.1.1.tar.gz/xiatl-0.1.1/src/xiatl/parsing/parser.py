from xiatl.parsing.pegboard.core.transforms import *
from xiatl.parsing.pegboard import generate_parser
from importlib import resources

grammar_string = resources.files("xiatl.parsing").joinpath("grammar.peg").read_text()
parser = generate_parser(start_symbol="input", grammar_string=grammar_string)

xiatl_transforms = {
        "word_literal" : sequential(pool,rename("LITERAL")),
        "standard_literal" : sequential(pool, rename("LITERAL")),
        "signature_literal" : sequential(pool, rename("LITERAL")),
        "verbatim_literal" : sequential(pool, rename("LITERAL")),
        "comment_literal" : sequential(pool, rename("LITERAL")),
        "string_literal_1" : sequential(pool, rename("LITERAL")),
        "string_literal_2" : sequential(pool, rename("LITERAL")),
        "inline_delimiter" : sequential(pool, rename("LITERAL")),
        "whitespace" : sequential(pool, rename("WHITESPACE")),
        "node_type" : sequential(pool, rename("NODE_TYPE")),
        "node_name" : sequential(pool, rename("NODE_NAME")),
        "node_tag" : sequential(pool, rename("NODE_TAG")),
        "inargument_scope" : rename("scope"),
        "inargument_item" : rename("item"),
        "any" : sequential(pool, rename("LITERAL")),
        "python_code" : sequential(pool, rename("PYTHON_CODE")),
        "macro_close" : sequential(pool, rename("MACRO_CLOSE")),
        "macro_open" : sequential(pool, rename("MACRO_OPEN")),
        "colon" : sequential(pool, rename("LITERAL")),
        "brac_group" : sequential(pool, rename("LITERAL")),
        "paren_group": sequential(pool, rename("LITERAL")),
        "curl_group": sequential(pool, rename("LITERAL")),
}
