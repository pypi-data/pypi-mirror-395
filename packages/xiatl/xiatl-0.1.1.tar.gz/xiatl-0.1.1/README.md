# XIATL — eXtensible Intuitive Automatable Tree Language

XIATL is a lightweight language designed for encoding structured information in plain text, with a focus on ergonomics, flexibility, and automation. 

XIATL lets you write:
- **Tree Structures** using a comfortable, minimal syntax
- **Macros** with flexible, readable signatures
- **Inline Python** fully compatible with the full Python ecosystem
- **Cross-Structure References** for encoding graph-like relationships  

A XIATL string is parsed and loaded in Python as a tree of Node objects of the form:

```python
Node(
    type: str,
    name: str | None,
    tags: list[str],
    children: list[Node | str],
    parent: Node | None
)
```

Beyond that, XIATL **imposes no data model**. There are no built-in node types or post-processing routines. You decide what node types you want and how to interpret/process them. XIATL is designed to be **comfortably human-writable**, not just human-readable. It's intended to allow semi-technical users (students, non-software professionals & academics, hobbyists, etc.) to easily encode and process information by providing a common foundation on which to build modular and interoperable encoding standards. 

XIATL combines:
* the extensibility of XML
* the convenience of LaTeX macros
* the computational flexibility of Python
* the minimalism of Markdown

XIATL comes with a **built-in debugger** to make the many automation features easier to use. Future updates will also include a **fully-featured suite of tree traversal and manipulation utilities** as well as **schema definition and validation** functionality.

Additionally, though this initial proof-of-concept release is implemented and heavily tied to the Python ecosystem, the ultimate goal is to make make XIATL **independent of any one ecosystem**. The exact mechanics of this are TBD, but the current idea is to rewrite the engine using a more performant low-level language, and replace inline Python with a lightweight Python-like scripting language. Bindings would then be supplied for different ecosystems (Python, JavaScript, C++, etc). This approach would have the additional security benefit of allowing inline code to be sandboxed.

## Example
```xiatl
$ author >> John Doe $$ # <- basic macro definition

::: # <- inline Python block
from datetime import date
today = date.today().strftime("%B %d, %Y")
:::

log <
    title < Field Notes >
    metadata <
        author < `author > # <- shorthand macro call
        date < ::today > # <- shorthand inline python access
    >
    observations <
        item < early wildflowers >
        item < low water levels >
        item < red-throated loon sighting >
    >
>
```

## Installation

XIATL is written in pure Python and depends only on Python's standard library. Currently, XIATL has been tested only on Python 3.13, but is expected to run on much older platforms as well. It can be installed directly from PyPI by running:

```bash
pip install xiatl
```

### Security Notice
> Parsing XIATL files/strings executes inline code using Python's `exec()`.
> **These files can execute arbitrary Python code.**
> Only parse XIATL files/strings from trusted sources, just as you would with any Python script.

## Usage
```python
import xiatl

# Load a file
result = xiatl.load_file("some_file.xiatl")
print(result.to_string())

# Resolve a file (resolve macros and inline Python only, tree not built)
result = xiatl.resolve_file("some_file.xiatl")
print(result)

# Load a project
result = xiatl.load_project("project_dir")
print(result.to_string())

# Load a string
input_string = """
$ name >> John Doe $$

object <
    author < `name >
    survey <
        location <North Ridge Wetlands>
        date <2025-03-14>
        observations <
          i< low water levels >
          i< three red-throated loons >
          i< early wildflowers >
        >
    >
    contact <john.doe\@example.com>
>
"""
result = xiatl.load_string(input_string)
print(result.to_string())

# Resolve a string (resolve macros and inline Python only, tree not built)
result = xiatl.resolve_string(input_string)
print(result)

# Manually Assemble Project
tree_1 = xiatl.load_file("file_1.xiatl")
tree_2 = xiatl.load_file("file_2.xiatl")
project_root = xiatl.Node(node_type=xiatl.PROJECT_ROOT, name="my_project",
                          children=[tree_1, tree_2])
xiatl.finalize_project_tree(node=project_root, project_root=project_root)
print(project_root.to_string())
```

## Why Macros + Inline Python?
A valid question that may arise is: "Why have both macros and inline Python execution if Python is already powerful enough?". The answer is that macros provide a tool for automation with simple mechanics that are more approachable for non-programmers (think LaTeX in academia). Though the development of useful systems that employ XIATL will require "real programming," it is not expected that the majority of the *users* of those systems will be familiar with programming. Since XIATL macros are completely compatible with inline Python, developers of the XIATL ecosystem can hide complex functionality written in Python and expose it through macros.

## Stability & Roadmap
XIATL is still in early development. Due to various time constraints, a stable release is expected no earlier than January 2027. Planned pre-stable-release updates currently include:

* major engine overhaul (redesigned for performance and portability)
* schema definition (in XIATL) and validation (with API), could significantly improve performance
* grammar improvements (fix annoying quirks in node grammar that slow down parsing)
* tree traversal/manipulation utility suite
* major parser improvements (currently very slow with basic recursive descent PEG parsing, will switch to Packrat parsing)
* major debugger improvements (including inline code debugging)
* improved error messages
* syntax highlighting plugins for Vim, VSCode, etc

## Contributing
Feedback, ideas, and discussion are always welcome!
However, because the project is still in an early design phase, we're **not yet accepting general contributions**. Contribution opportunities will open once the core cross-platform engine components are complete (estimated late 2026). At that point, governance will follow a BDFN (Benevolent Dictator For Now) model (similar to Zig's approach), which means that [id.est.2817.2](https://codeberg.org/id_est_2817_2) will have final say in design and implementation.
That said, if you're interested in being involved long-term, feel free to reach out at id.est.2817.2@gmail.com. While we can't guarantee immediate opportunities, we're happy to hear from people who are excited about the project, and we'd be glad to discuss involvement opportunities personally.

## Reference

### Table of Contents
- [Literals](#literals)
- [Nodes](#nodes)
- [Macros](#macros)
- [Comments](#comments)
- [Inline Python](#inline-python)
- [Node References](#node-references)
- [Structural Model](#structural-model)
- [Debugger](#debugger)
- [Comparative Examples](#comparative-examples)

### Literals

A **literal** is any sequence of non-whitespace, non-reserved characters:

```
hello
42
abc_def
really?
yeah!
"apple"
I'm
hungry
now.
```

A **word literal** is any sequence of letters, numbers, or underscores. This distinction is important for contexts in which only word literals are accepted (node types, names, tags, among others).

The set of **standard reserved characters** includes `<`, `>`, `#`, `@`, `` ` ``, `$` as well as the symbol `:::`.

The **expanded set of reserved characters** (for use in macro signatures) includes all of the above in addition to `:`, `(`, `)`, `,` as well as the symbols `>>` and `<<`.

All escaped reserved characters are **accepted if they are escaped** with a **backslash** (e.g., `\<`).

**Whitespace** (including multiple newlines) is almost always treated as a delimiter between literals (save for a few special contexts) and has no semantic meaning.

To include whitespace or special characters in a literal, wrap text in backticks to create a **verbatim literal**:

```
``This verbatim literal stays
        exactly
as written``

``This one contains an escaped backtick: \` ``

``This one contains some reserved characters <>$@``
```

Verbatim literals are preserved exactly. In general, all literals are parsed and included in the
final tree as leaf nodes (children of the node they are in).

[Back to Table of Contents ↑](#table-of-contents)
### Nodes

Nodes look like HTML/XML but without reserved keywords or angle-bracket escaping.

```
header < This is a header >
paragraph < Some text in a paragraph >
```
The general syntax of a  node is:

```
node_type [optional node name] {optional, ordered, comma, delimited, tags} < children...>
```
* The **node type** is a **single word literal**
* The **node name** is **any sequence of word literals and whitespace** (entire sequence is saved as the node name, including whitespace), and **must be unique** among the node's siblings.
* **Node tags** are **each a sequence of word literals and whitespace** (whitespace is meaningful), are ordered, and have no uniqueness requirements.
* The **children** of the node may be **literals or other nodes**.
* The **body** of the node (inside the angle brackets) **creates a scope** (used by macros and inline Python).

#### Examples

Encoding a tiny document structure:
```
document <
    header < Welcome >
    A quick line of text after the header...
    paragraph < Here is the contents of a paragraph >
    footer <>
>
```
Now with names and tags:
```
document [My Introductory Document]
{training materials, easy, super cool} <
    header < Welcome >
    A quick line of text after the header...
    paragraph [First] < Hello! >
    paragraph [Second] < Another paragraph. >
    footer <>
>
```
There are no pre-defined node types. Use whatever best fits your data!
```
log [My Unicorn Sighting Log] <
    entry {failure} <
        date < 02 10 2307 >
        title < no luck >
        we saw no unicorns today :(
    >
    entry {success} <
        date < 02 11 2307 >
        title < huzzah! >
        we saw a unicorn today! :)
    >
>
```

[Back to Table of Contents ↑](#table-of-contents)
### Macros

XIATL includes a powerful macro system inspired by LaTeX, but more ergonomic.

We define a simple replacement macro:

```
$ quantity >> 34098 $$
```
and call it:

```
I bought $ quantity $$ apples.
```

The above expands to:

```
I bought 34098 apples.
```

Everything after `>>` and before `$$` in the macro definition is the **body** of the macro, and defines its lexical scope. The body of a macro (and any macros therein) are expanded at call time, and with respect to the scope they are called in (i.e., macro bodies do not capture macro definitions at the time they are defined and instead rely on the defintions of macros existing in the scope they are called).

#### Arguments & Parameters
Macros can be defined with **parameters** (accessed with **parameter reference** syntax `@(parameter name)` in macro body). **Parameter names** can be composed of **any sequence of literals and whitespace** (whitespace is meaningful). Parameter references in the body of the macro are simple replacements (i.e., the passed argument is pasted "as is" in place of the reference at macro call time).

```
$ greet (name) >> Hello @(name)! $$
$ introduce (name 1, name 2) >>  @(name 1), meet @(name 2)! $$
```

The **arguments** in macro calls can be **any sequence of literals or whitespace**. In fact, argument fields (i.e., the spaces between the commas in argument lists) **each create a scope** that is resolved before the rest of the macro call, meaning macros and inline code can be used to generate the arguments.

```
$ him >> Carl Friedrich Gauss $$
$ her >> Ada Lovelace $$
$ greet ($him$$) $$
$ introduce ($him$$, $her$$) $$
```
The above expands to
```
Hello Carl Friedrich Gauss!
Carl Friedrich Gauss, meet Ada Lovelace!
```
Macro parameters can also be defined with default values (using `<<` for assignment):

```
$ greet (name << stranger) >> Hello @(name)! $$
$ greet () $$
```
The above expands to
```
Hello stranger!
```
In general, macro parameter/argument semantics behave almost exactly like Python function parameters/arguments (except for `*args` and `**kwargs` which are not yet supported).
```
$ greet (name << stranger, greeting << Hi!) >> @(greeting), @(name)! $$
$ greet (greeting << Fancy meeting you here) $$ 
```
The above expands to
```
Fancy meeting you here, stranger!
```

#### Signatures
Macro signatures are actually defined as **whitespace-delimited sequences of literals and parameter lists**, which allows them to take on very natural shapes:

```
$ introduce (a) to (b) >> @(a), meet @(b). $$
$ eagerly introduce (x) to (y) >> @(x), meet the amazing @(y)! $$
```

Call:

```
$ introduce (John) to (Sarah) $$
$ eagerly introduce (John) to (Sarah) $$
```

Expands to:

```
John, meet Sarah.
John, meet the amazing Sarah!
```
The **literals in macro signatures** can include any character except those in the **extended reserved character set**.

#### Shorthand Call Syntax
Macros with a **single literal in their signature** and **no parameters** (like the `quantity` example macro above) can be called with a simple shorthand:

```
`quantity
```

No whitespace is allowed after the backtick.

[Back to Table of Contents ↑](#table-of-contents)
### Comments
XIATL line comments look and work exactly like Python line comments:

```
# this is a comment
```

[Back to Table of Contents ↑](#table-of-contents)
### Inline Python

Inline Python execution is delimited by the `:::` symbol:

```
:::
print("hello from python")
:::
```

The block is **executed, then discarded**. The string is printed to stdout, just as in regular Python. It is **not automatically inserted** into the XIATL file. To insert files, use the provided `insert()` function (available in all inline Python contexts):

```
:::
x = "Inserted text"
insert(x)
a = 1
b = 2
insert(a,b)
:::
```
The above block would be executed and replaced with the inserted items.
You can easily define functions as well:

```
:::
def f(x,y):
    return x+y

insert(f(10,1))
:::
```
#### Scoping Rules
* Python blocks **do not** create new scopes on their own.
* Python runs inside the **current XIATL scope** (definitions persist throughout the XIATL scope)
* Python blocks in general do not have access to Python definitions of parent XIATL scopes (just as Python functions do not by default have access to definitions above them in the call stack). The only exception is global defininitions made at the file-scope level (just as in Python).
* XIATL file scope behaves like Python file scope (creates global definitions).

#### Shorthand Insert Syntax
You can run and insert the result of Python expressions concisely:

```
::x
::f(a,b)
```
This shorthand is conveninent for inserting values anywhere:

```
Sum is ::f(a,b)
```
The above expands to:
```
Sum is 3
```
This shorthand does not currently support nested expressions.


#### Combining Macros & Inline Python
Macros and inline Python can be combined to create powerful functionality with simple interfaces. Inline Python blocks inside the body of a macro may access the arguments of the macro through the provided `arguments()` function. Unlike argument references, arguments accessed with the `arguments()` function are parsed and loaded as local trees (see [Structural Model](#structural-model)). This creates a clear separation of concerns that maximizes the utility of both methods of automation: macros function exclusively in the textual domain and inline Python in the object domain.

Below is an example of a macro that makes use of inline Python to mark a series of log entries with a `loadtime` stamp. The macro also inserts a reference (see [Node References](#node-references)) to the literal child `this` of the node named `initial entry`.

```xiatl
$ add loadtimes (log) >>
    :::
    from xiatl import Node, Node_Reference
    from time import time
    
    for item in argument("log"):
        if item.node_type == "entry":
            current_time = str(time())
            loadtime = Node(node_type="loadtime", children=[current_time])
            item.children.append(loadtime)
        insert(item)

    insert(Node_Reference(components = ["initial entry", 0]))
    :::
$$
```
We may use the macro as:

```xiatl
$ add loadtimes (
    entry [initial entry] < this is a log entry >
    entry < this is another log entry >
    entry < this is third log entry >
  )
$$
```
which expands into (prettyfied for illustration):

```xiatl
entry [initial entry] <
    this is a log entry
    loadtime < 1764704898.564757 >
>
entry < this is another log entry
        loadtime < 1764704898.564767 >
>
entry < this is third log entry
        loadtime < 1764704898.56477 >
>
@[initial entry][0]
```

[Back to Table of Contents ↑](#table-of-contents)
### Node References

References let you refer to nodes or literal children anywhere in the tree, allowing for the encoding of graph-like structures. References are parsed and included in the node tree as objects of the form:

```python
Node_Reference(
    item: Node | str, # <- this is the actual item the reference points to
    parent: Node | None
)
```

Basic form:

```
@[Name or index of node or literal in this scope]
```

Names refer to **named nodes**, indices are **0-based** and refer to **any child** (node or literal), both resolve relative to the **current scope**. The file scope is the scope of the local tree root (see [Structural Model](#structural-model)). You can build "paths" further into the tree by **chaining names or indices** (you can think of these like file paths in a file tree):

```
@[Doc][First Paragraph][1]
```

Reference paths can begin with a few special components:

* `[^]` – refers to the scope above the current scope
* `[^^]` – refers to the local root (see [Structural Model](#structural-model))
* `[^^^]` – refers to the project root (see [Structural Model](#structural-model))

These special path components can only be used at the beginning of the path. This keeps references easier to read and reason about. Spaces between the components or after the `@` symbol are not allowed (e.g., `@ [^] [a node]` will not parse).

[Back to Table of Contents ↑](#table-of-contents)
### Structural Model

XIATL is being designed to be **structurally independent of any file system**. XIATL input may be loaded into Python using either the `load_string(input_string)` or `load_file(filename)` functions. In either case, any single XIATL input string is loaded into a **local tree**, whose root is of type `^^`. If using the `load_file(filename)` function, the name of the local root node is set to the file stem (i.e., file name minus the `.xiatl` extension). A **project tree** is a composed of multiple **local trees**. A project may be loaded using either `load_project(dirname)`, or manually assembled by connecting previously loaded local trees and running `finalize_project_tree(node, project_root)` to resolve project-wide references. When using `load_project(dirname)`, the given directory is read recursively, loading all `.xiatl` files into a project tree structure. Intermediate directories are loaded as nodes whose children are either local trees defined by XIATL files or nodes from other intermediate directories.


[Back to Table of Contents ↑](#table-of-contents)
### Debugger

Complex macro systems are often the source of much confusion and reliability issues. To help mitigate this, XIATL comes with a built-in debugger. To drop into it, simply insert a breakpoint:

```
@breakpoint
```

Currently, the debugger supports:

* stepping through macro expansions
* viewing macro definitions available in the current scope

Future releases will also support inline code debugging and inspection of the partially-built node tree.

[Back to Table of Contents ↑](#table-of-contents)
### Comparative Examples
Here are some example files in LaTeX, HTML, SVG, JSON, and Markdown, alongside examples of what encoding the same data in XIATL might look like.

#### LaTeX
```latex
\documentclass{article}
\usepackage{amsmath}

\title{A Short Calculation}
\author{John Doe}

\begin{document}
\maketitle

We recall the Gaussian integral
\[
I = \int_{-\infty}^{\infty} e^{-x^2}\,dx.
\]

Switching to polar coordinates gives
\[
I^2 = \int_0^{2\pi}\!\!\int_0^\infty e^{-r^2} r\,dr\,d\theta = \pi,
\]
so $I = \sqrt{\pi}$.

\end{document}
```

#### XIATL
```xiatl
title < A Short Calculation >
author < John Doe >

document {article} <
    We recall the Gaussian integral
    math {disp} <
        I = int<-infty ^ infty> exp<-pow<x ^ 2>> dx.
    >
    Switching to polar coordinates gives
    math{disp}<
        pow<I 2> = int<0 ^ 2 pi>  int<0 ^ infty> exp<-pow<r 2>> r d<r> d<theta> = pi,
    >
    so math{line}<I = sqrt<pi>>.
>
```

[Back to Table of Contents ↑](#table-of-contents)

---

#### HTML
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Notes — John Doe</title>
  <style>
    body { font-family: Georgia, serif; margin: 30px; }
  </style>
</head>
<body>

<h1>Notes</h1>

<p>John Doe recorded several early flowering plants along the creek,
including trout lilies and wood anemones.</p>

<ul>
  <li>Low water levels</li>
  <li>Frequent sparrow activity</li>
</ul>

<p>Contact: <a href="mailto:john.doe@example.com">email</a></p>

</body>
</html>
```

#### XIATL
```xiatl
doctype<html>
html<
    lang<en>
    head<
        charset<UTF-8>
        title<Notes - John Doe> 
        style<
            body < font<Georgia serif> margin<30 px> >
        >
    >
    body <
        h1<Notes>
        p<John Doe recorded several early flowering plants along the creek,
        including trout lilies and wood anemones.>
        ul<
          li<Low water levels>
          li<Frequent sparrow activity>
        >
        p<Contact: a<href<mailto<john.doe\@example.com>>  email>>
    >
>
```
[Back to Table of Contents ↑](#table-of-contents)

---

#### SVG
```svg
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="200" height="140" viewBox="0 0 200 140">

  <rect x="0" y="0" width="200" height="140" fill="#f5f5f5"/>

  <circle cx="160" cy="30" r="15" fill="#ffd86b"/>

  <rect x="40" y="80" width="10" height="25" fill="#8b5a2b"/>
  <circle cx="45" cy="70" r="18" fill="#4c7a3d"/>

  <path d="M 10 140 Q 60 90 190 120"
        stroke="#c69c6d" stroke-width="4" fill="none"/>

</svg>
```

#### XIATL
```xiatl
version<1.0>
encoding<UTF-8>
svg<
    width<200> height<140> viewBox<0 0 200 140>

    rect<  x<0> y<0> width<200> height<140> fill{hex}<f5f5f5>  >

    circle<  cx<160> cy<30> r<15> fill{hex}<ffd86b>  >

    rect<  x<40> y<80> width<10> height<25> fill{hex}<8b5a2b>  >
    circle< cx<45> cy<70> r<18> fill{hex}<4c7a3d>  >

    path< d<M 10 140 Q 60 90 190 120>
        stroke{hex}<c69c6d> stroke_width<4> fill<none>  >
>
```
[Back to Table of Contents ↑](#table-of-contents)

---

#### JSON
```json
{
  "author": "John Doe",
  "survey": {
    "location": "North Ridge Wetlands",
    "date": "2025-03-14",
    "observations": [
      "low water levels",
      "three red-throated loons",
      "early wildflowers"
    ]
  },
  "contact": "john.doe@example.com"
}
```

#### XIATL
```xiatl
object <
    author < John Doe >
    survey <
        location <North Ridge Wetlands>
        date <2025-03-14>
        observations <
          i< low water levels >
          i< three red-throated loons >
          i< early wildflowers >
        >
    >
    contact <john.doe\@example.com>
>
```
[Back to Table of Contents ↑](#table-of-contents)

---

#### Markdown
```markdown
# Field Notes — John Doe

Early in the season, several migratory birds were seen near the west marsh.
Water levels remained below average throughout the week.

## Observations

- Three sandpipers along the inlet
- Sparse vegetation on the north bank
- First signs of emerging wildflowers

For more details, contact **john.doe@example.com**.
```

#### XIATL
```xiatl
heading <Field Notes — John Doe>

Early in the season, several migratory birds were seen near the west marsh.
Water levels remained below average throughout the week.

subheading <Observations>

li<Three sandpipers along the inlet>
li<Sparse vegetation on the north bank>
li<First signs of emerging wildflowers>

For more details, contact b<john.doe\@example.com>.
```
[Back to Table of Contents ↑](#table-of-contents)

---

## License
   Copyright 2025 id.est.2817.2

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
