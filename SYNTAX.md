## Syntax

> - `?` after an item means `0 or 1`
> - `*` after an item means `0 or many`
> - `+` after an item means `1 or many`
> - `( )` group items.
> - Things in code are terminals, just words/symbols - nonterminals.
> - Nonterminals in italic are too obvious to define.
> - Nonterminals in bold will be defined in future.

---

start ::= module+ .

module ::= `module` _ident_ module_block .

module_block ::=
`{`
    `connections:`
        (import | use)*
    `types:`
        (type | typedef | interface | suit)*
    `fields:`
        (var | let)*
    (`extend` _ident_ `:`
        ((func | proc)+ | (funcdecl `;`)+)
    )*
    `functions:`
        def+
`}` .

---

import ::= `import` _ident_ `;` .

use ::= `use` _ident_ `;` .

---

type ::= `type` typename `=` (product | variant | intersection | functional) `;` .

typename ::= _ident_ generic .

generic ::= (`<` _ident_ (`,` _ident_)* `>`)? .

product ::= (`*` formal)+ .

formal ::= _ident_ `:` typename .

variant ::= (`|` _ident_ typename)+ .

intersection ::= `&` typename (`&` intervar)+ .

intervar ::= typename | formal | product .

functional ::= `(` typenames_list `)` `:` typename .

typenames_list = typename (`,` typename)+ .

typedef ::= `typedef` _ident_ `=` typename `;` .

interface ::= `interface` _ident_ `{` (funcdecl `;`)+ `}` .

suit ::= `suit` _ident_ `:` (_ident_ | variant) .

---

var ::= `var` naming .

let ::= `let` naming .

naming ::= _ident_ (`:` _ident_ `=` x_expr | `=` (_data_ | new)) `;` .

new ::= `new` funcall .

funcall ::= _ident_ `(` (_expr_ (`,` _expr_)*)? `)` .

---

def ::= func | proc | pure | cort .

func ::= `func` funcimpl .

proc ::= `proc` _ident_ `(` formals_list `)` code_block .

pure ::= `pure` funcimpl .

cort ::= `cort` funcdecl code_block .

funcimpl ::= funcdecl (code_block | `=>` x_expr `;`) .

funcdecl ::= _ident_ `(` formals_list `)` `:` typename .

formals_list ::= (formal (`,` formal)*)? .

---

x_expr ::= _expr_ | if_expr | pipe_expr | **lambda** | **matchexpr** | **comprehension** .

if_expr ::= `if` _expr_ `:` x_expr (`elif` _expr_ `:` x_expr)* `else` `:` x_expr .

pipe_expr ::= (_expr_ | pipe_expr) `|>` (_ident_ | funcall) .

---

code_block ::= `{` (var | let | mod | loops | if | proc_call | return | **del** | **matchstat**)+ `}` .

mod ::= `mod` _ident_ _assignop_ x_expr `;` .

loops ::= (loop | while | until | for) code_block | `do` code_block (while | until) `;` .

loop ::= `loop` .

while ::= `while` _expr_ .

until ::= `until` _expr_ .

for ::= `for` _ident_ `in` (_container_ | _ident_ | funcall) .

if ::= `if` _expr_ code_block (`elif` _expr_ code_block)* (`else` code_block)? .

proc_call ::= `call` (funcall | pipe_expr) `;` .

return ::= `return` x_expr `;` .
