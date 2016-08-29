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
        ((func | proc)+ | (func_decl `;`)+)
    )*
    `functions:`
        functions+
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

interface ::= `interface` _ident_ `{` (func_decl `;`)+ `}` .

suit ::= `suit` _ident_ `:` (_ident_ | variant) .

---

var ::= `var` naming .

let ::= `let` (naming | _ident_ `=` lambda) .

naming ::= _ident_ (`:` _ident_ `=` (x_expr - lambda) | `=` (_data_ | new)) `;` .

new ::= `new` func_call .

func_call ::= _ident_ `(` (x_expr (`,` x_expr)*)? `)` .

---

functions ::= func | proc | pure | cort .

func ::= `func` func_impl .

proc ::= `proc` _ident_ `(` formals_list `)` func_code_block .

pure ::= `pure` func_impl .

cort ::= `cort` func_decl func_code_block .

func_impl ::= func_decl (func_code_block | `=>` x_expr `;`) .

func_decl ::= _ident_ `(` formals_list `)` `:` typename .

formals_list ::= (formal (`,` formal)*)? .

---

x_expr ::= _expr_ | if_expr | pipe_expr | lambda | match_expr | comprehension .

if_expr ::= `(` `if` _expr_ `:` x_expr (`elif` _expr_ `:` x_expr)* (`else` `:` x_expr)? `)` .

pipe_expr ::= x_expr `|>` (_ident_ | func_call | lambda) .

lambda ::= `lambda` `(` formals_list `)` (`:` typename `=>` (x_expr - lambda) | `=>` lambda) .

match_expr ::= `match` _ident_ `{` (_expr_ `:` x_expr `;`)+ (`else:` x_expr `;`)? `}` .

comprehension ::= `[` for `:` (_expr_ | if_expr | pipe_expr) `]` .

---

func_code_block ::= `{` (statements | def)+ `}` .

statements = var | let | mod | loop | if | proc_call | return | del | match_stat .

code_block ::= `{` (statements | _break_ | _continue_)+ `}` .

mod ::= `mod` _ident_ _assignop_ x_expr `;` .

loop ::= (`loop` | while | until | for) code_block | `do` code_block (while | until) `;` .

while ::= `while` _expr_ .

until ::= `until` _expr_ .

for ::= `for` _ident_ `in` (_container_ | _ident_ | func_call) .

if ::= `if` _expr_ code_block (`elif` _expr_ code_block)* (`else` code_block)? .

proc_call ::= `call` (func_call | pipe_expr) `;` .

return ::= `return` x_expr `;` .

del ::= `del` _ident_ .

match_stat ::= `match` _ident_ `{` (_expr_ `:` code_block)+ (`else:` code_block)? `}` .

def = `def` func_impl .
