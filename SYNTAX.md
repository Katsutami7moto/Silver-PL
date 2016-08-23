## Syntax (RBNF)

> `[ ]` means `0 or 1`
> `{ }` means `1 or many`
> `[{ }]` means `0 or many`
> Things in code are terminals, just words/symbols - nonterminals
> Nonterminals in italic are obvious to define.
> Nonterminals in bold will be defined in future.

Start = { Module } .

Module = `module` _Ident_ ModuleBlock .

ModuleBlock = `{` { Import | Type | Typedef | **Interface** | **Suit** | Fields | Extend | Def } `}` .

Import = `import` _Ident_ `;` .

Type = `type` TypeName `=` ( Product | Variant | Intersection | Functional ) `;` .

TypeName = _Ident_ Generic .

Generic = [ `<` _Ident_ [{ `,` _Ident_ }] `>` ] .

Product = { `*` Formal } .

Variant = { `|` _Ident_ TypeName } .

Intersection = `&` TypeName { `&` InterVar } .

InterVar = TypeName | Formal | Product .

Functional = `(` TypeName { `,` TypeName } `)` `:` TypeName .

Typedef = `typedef` _Ident_ `=` TypeName `;` .

Fields = `fields` `{` { Var | Let } `}` .

Extend = `extend` _Ident_ ( `:` Def | `{` { Def } `}` ) .

New = `new` Call .

Def = `def` _Ident_ `(` [ Formal [{ `,` Formal }] ] `)` ( `:` TypeName ( CodeBlock | `=>` XExpr `;` ) | CodeBlock ) .

Formal = _Ident_ `:` TypeName .

CodeBlock = `{` { Var | Let | Mod | Loops | If | Call `;` | PipeExpr `;` | Return } `}` .

XExpr = _Expr_ | IfExpr | PipeExpr .

IfExpr = `if` _Expr_ `:` XExpr [{ `elif` _Expr_ `:` XExpr }] `else` `:` XExpr .

PipeExpr = ( _Expr_ | PipeExpr ) `|>` ( _Ident_ | Call ) .

Var = `var` Naming .

Let = `let` Naming .

Naming = _Ident_ ( `:` _Ident_ `=` XExpr | `=` ( _Data_ | New ) ) `;` .

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
