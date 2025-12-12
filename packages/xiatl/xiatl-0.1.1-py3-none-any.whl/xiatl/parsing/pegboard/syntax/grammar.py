from xiatl.parsing.pegboard.core.parser import *
from xiatl.parsing.pegboard.core.constants import *

syntax_terminals = {
    "POUND"               : r"#",
    "LEFTARROW"           : r"<-",
    "SLASH"               : r"/",
    "ASSERT"              : r"&",
    "REJECT"              : r"!",
    "QUESTION"            : r"\?",
    "STAR"                : r"\*",
    "PLUS"                : r"\+",
    "OPEN"                : r"\(",
    "CLOSE"               : r"\)",
    "ALPHA"               : r"[a-zA-Z_]",
    "WORDCHAR"            : r"\w",
    "WHITESPACE"          : r"\s+",
    "QUOTE"               : r"'",
    "QUOTES"              : r'"',
    "ANY_CHAR_NOT_QUOTE"  : r"[^']",
    "ANY_CHAR_NOT_QUOTES" : r'[^"]',
    "ANY_CHAR"            : r'.',
    "EOF"                 : EOF_MARKER,
    "EOL"                 : EOL_MARKER
}

syntax_non_terminals = {
    "Grammar"     : [SEQUENCE, [AT_LEAST_ZERO, [NON_TERMINAL, "Spacing"]], [AT_LEAST_ZERO, [NON_TERMINAL, "Definition"]], [EOF]],
    "Definition"  : [SEQUENCE, [NON_TERMINAL, "Identifier"], [NON_TERMINAL, "Spacing"], [TERMINAL, "LEFTARROW"], [NON_TERMINAL, "Spacing"], [NON_TERMINAL, "Expression"], [AT_LEAST_ZERO, [NON_TERMINAL, "Spacing"]]],
    "Identifier"  : [SEQUENCE, [TERMINAL, "ALPHA"], [AT_LEAST_ZERO, [TERMINAL, "WORDCHAR"]]],
    "Expression"  : [NON_TERMINAL, "Choice"],
    "Choice"      : [SEQUENCE, [NON_TERMINAL, "Sequence"], [AT_LEAST_ZERO, [SEQUENCE, [NON_TERMINAL, "Spacing"], [TERMINAL, "SLASH"], [NON_TERMINAL, "Spacing"], [NON_TERMINAL, "Sequence"]]]],
    "Sequence"    : [SEQUENCE, [NON_TERMINAL, "Prefixed"], [AT_LEAST_ZERO, [SEQUENCE, [NON_TERMINAL, "Spacing"], [NON_TERMINAL, "Prefixed"]]]],
    "Prefixed"    : [SEQUENCE, [OPTIONAL, [NON_TERMINAL, "Prefix"]], [NON_TERMINAL, "Suffixed"]],
    "Prefix"      : [CHOICE, [TERMINAL, "REJECT"], [TERMINAL, "ASSERT"]],
    "Suffixed"    : [SEQUENCE, [NON_TERMINAL, "Primary"], [OPTIONAL, [NON_TERMINAL, "Suffix"]]],
    "Suffix"      : [CHOICE, [TERMINAL, "PLUS"], [TERMINAL, "STAR"], [TERMINAL, "QUESTION"]],
    "Primary"     : [CHOICE, [TERMINAL, "EOF"], [TERMINAL, "EOL"], [SEQUENCE, [NON_TERMINAL, "Identifier"], [REJECT, [SEQUENCE, [OPTIONAL, [NON_TERMINAL, "Spacing"]], [TERMINAL, "LEFTARROW"]]]], [NON_TERMINAL, "Grouping"], [NON_TERMINAL, "Pattern"]],
    "Grouping"    : [SEQUENCE, [TERMINAL, "OPEN"], [OPTIONAL, [NON_TERMINAL, "Spacing"]], [NON_TERMINAL, "Expression"], [OPTIONAL, [NON_TERMINAL, "Spacing"]], [TERMINAL, "CLOSE"]],
    "Pattern"     : [SEQUENCE, [CHOICE, [SEQUENCE, [TERMINAL, "QUOTE"], [AT_LEAST_ZERO, [TERMINAL, "ANY_CHAR_NOT_QUOTE"]], [TERMINAL, "QUOTE"]],
                                        [SEQUENCE, [TERMINAL, "QUOTES"], [AT_LEAST_ZERO, [TERMINAL, "ANY_CHAR_NOT_QUOTES"]], [TERMINAL, "QUOTES"]]]],
    "Spacing"     : [AT_LEAST_ONE, [CHOICE, [TERMINAL, "WHITESPACE"], [NON_TERMINAL, "Comment"]]],
    "Comment"     : [SEQUENCE, [TERMINAL, "POUND"], [AT_LEAST_ZERO, [SEQUENCE, [REJECT, [EOL]], [TERMINAL, "ANY_CHAR"]]], [EOL]]
}

