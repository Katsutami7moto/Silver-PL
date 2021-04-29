## Syntax

> - `?` after an item means `0 or 1`
> - `*` after an item means `0 or many`
> - `+` after an item means `1 or many`
> - Infix `-` means `except`
> - `( )` group items.
> - Things in code are terminals, just words/symbols - nonterminals.
> - Nonterminals in italic are too obvious to define.
> - Nonterminals in bold will be defined in future.

---

start ::= module+ .

module ::= `module` point_idents `;` module_block .

point_idents ::= _ident_ ( `.` _ident_ )* .

module_block ::=
(`connections:`
    (import | use)
)*
(`types:`
    (type | typedef | interface)
)*
(`fields:`
    (var | let)
)*
(`extend` _ident_ `:`
    ( (func | proc)+ | (func_decl `;`)+ )
)*
`functions:`
    functions+
.

---

import ::= `import` point_idents `;` .

use ::= `use` point_idents `;` .

---

type ::= `type` typename `=` (product | variant | intersection | functional) methods `;` .

methods ::= `methods:` functions+ .

typename ::= _ident_ generic .

generic ::= (`<` _ident_ (`,` _ident_)* `>`)? .

product ::= (`*` formal)+ .

formal ::= _ident_ `:` typename .

variant ::= (`|` _ident_ typename)+ .

intersection ::= `&` typename (`&` intervar)+ .

intervar ::= typename | formal .

functional ::= `(` typenames_list `)` `:` typename .

typenames_list = typename (`,` typename)+ .

typedef ::= `typedef` _ident_ `=` typename `;` .

interface ::= `interface` typename (`=` intersection )? methods `;` .

---

var ::= `var` naming .

let ::= `let` naming.

naming ::= _ident_ (`:` _ident_ `=` x_expr | `=` (_data_ | new)) `;` .

new ::= `new` func_call .

func_call ::= _ident_ `(` (x_expr (`,` x_expr)* )? `)` .

---

functions ::= func | proc | pure | cort | cell .

func ::= `func` func_impl .

proc ::= `proc` _ident_ `(` formals_list `)` code_block .

pure ::= `pure` func_impl .

cort ::= `cort` func_decl code_block .

cell ::= `cell` _ident_ `:` typename (code_block | `=>` (x_expr - lambda) `;`) .

func_impl ::= func_decl (code_block | `=>` x_expr `;`) .

func_decl ::= _ident_ `(` formals_list `)` `:` typename .

formals_list ::= (formal (`,` formal)*)? .

---

x_expr ::= _expr_ | self | home | if_expr | pipe_expr | method_expr | lambda | match_expr | comprehension .

self ::= `self.` (_ident_ | func_call) .

home ::= `home.` (_ident_ | func_call) .

if_expr ::= `(` `if` _expr_ `:` x_expr (`elif` _expr_ `:` x_expr)* (`else` `:` x_expr)? `)` .

pipe_expr ::= x_expr `|>` (_ident_ | func_call | method_expr | lambda) .

method_expr ::= point_idents `.` func_call .

lambda ::= `lambda` `(` formals_list `)` (`:` typename `=>` (x_expr - lambda) | `=>` lambda) .

match_expr ::= `match` _ident_ `{` (_logop_ _expr_ `:` x_expr `;`)+ (`else:` x_expr `;`)? `}` .

comprehension ::= `[` for `:` (_expr_ | if_expr | pipe_expr) `]` .

---

code_block ::= `{` (statements+ | `break;` | `continue;` | return) `}` .

statements ::= var | let | mod | loop | if | proc_call | del | match_stat .

mod ::= `mod` _ident_ _assignop_ x_expr `;` .

loop ::= (`loop` | while | until | for) code_block | `do` code_block (while | until) `;` .

while ::= `while` _expr_ .

until ::= `until` _expr_ .

for ::= `for` _ident_ `in` (_container_ | _ident_ | func_call) .

if ::= `if` _expr_ code_block (`elif` _expr_ code_block)* (`else` code_block)? .

proc_call ::= `call` (func_call | pipe_expr | method_expr) `;` .

return ::= `return` x_expr `;` .

del ::= `del` _ident_ .

match_stat ::= `match` _ident_ `{` (_logop_ _expr_ `:` code_block)+ (`else:` code_block)? `}` .

## Algorithm of compiler

1. Turn a source code file into list of text lines
2. Turn the list of text lines into list of structured lexems (tokens)
3. Divide list of tokens by modules into several lists of tokens
4. Parse all modules' lists of tokens to make lists of modules' declarations (abstract data types) and to make symbol table
5. Using symbol table, parse again all modules' lists of tokens to make lists of modules' function definitions (abstract data types)
6. Process all lists of modules' declarations to make C code of forward declarations
7. Process all lists of modules' function definitions to make C code of functions definitions
8. Compose C code of declarations and definitions into a file and compile this file
