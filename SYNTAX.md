## Syntax (RBNF)

> `[ ]` means `0 or 1`
> `{ }` means `1 or many`
> `[{ }]` means `0 or many`
> Things in code are terminals, just words/symbols - nonterminals

Start = { Module } .

Module = `module` _Ident_ ModuleBlock .

ModuleBlock = `{` { Use | Import | Type | Typedef | Extend | Var | Let | Def } `}` .

Use = `use` _Ident_ `;` .

Import = `import` _Ident_ `;` .

Type = `type` _Ident_ Generic `=` ( Product | Variant | Intersection | **Functional** ) `;` .

Generic = [ `<` _Ident_ [{ `,` _Ident_ }] `>` ] .

Product = Formal [{ `*` Formal }] .

Variant = _Ident_ `|` _Ident_ [{ `|` _Ident_ }] .

Intersection = _Ident_ `&` InterVar [{ `&` InterVar }] .

InterVar = _Ident_ | Formal | Product .

Typedef = `typedef` _Ident_ `=` _Ident_ Generic `;` .

Extend = `extend` _Ident_ ( `:` Def | `{` { Def } `}` ) .

Var = `var` Naming .

Let = `let` Naming .

Naming = _Ident_ ( `:` _Ident_ `=` XExpr | `=` ( _Data_ | New ) `;` ) .

New = `new` Call .

Def = `def` _Ident_ `(` [ Formal [{ `,` Formal }] ] `)` ( `:` _Ident_ ( CodeBlock | `=>` XExpr `;` ) | CodeBlock ) .

Formal = _Ident_ `:` _Ident_ .

CodeBlock = `{` { Var | Let | Mod | Loops | If | Call `;` | PipeExpr `;` | Return } `}` .

XExpr = _Expr_ | IfExpr | PipeExpr .

IfExpr = `if` _Expr_ `:` XExpr [{ `elif` _Expr_ `:` XExpr }] `else` `:` XExpr .

PipeExpr = ( _Expr_ | PipeExpr ) `|>` ( _Ident_ | Call ) .

Mod = `mod` _Ident_ _AssignOp_ XExpr `;` .

Loops = Loop | While | Until | DoWhile | DoUntil | For CodeBlock .

Loop = `loop` CodeBlock .

While = `while` _Expr_ CodeBlock .

Until = `until` _Expr_ CodeBlock .

DoWhile = `do` CodeBlock `while` _Expr_ `;` .

DoUntil = `do` CodeBlock `until` _Expr_ `;` .

For = `for` _Ident_ `in` ( _Container_ | _Ident_ | Call ) .

If = `if` _Expr_ CodeBlock [{ `elif` _Expr_ CodeBlock }] [ `else` CodeBlock ] .

Call = _Ident_ `(` [ _Expr_ [{ `,` _Expr_ }] ] `)` .

Return = `return` XExpr `;` .
