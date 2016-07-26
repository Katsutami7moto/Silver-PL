# Silver
Silver is general-purpose programming language, which goal is to collect many useful features from other languages, but not to collect their design and work errors.

## Concepts

- Functional programming features: anonymous functions, first-class functions, closures, currying, partial application, orientation on programminng w/out variables
- Compound types and extension functions will make code more familiar to OOP-users
- No automatical/implicit type conversion, static strong type system
- No low-level looking basic types like `uint32`, this is unnecessary
- Silver compiler translates code to C language (C89 standart) for good portabilty and performance

## Features / TODO

- Literals
  - [x] Integer literals
  - [x] Floating point literals
  - [ ] List literals
  - [ ] String literals
  - [ ] Other containers literals
- Expressions
  - [x] Math expressions
  - [x] Logical expressions
  - [ ] Conditions `x in y`, `x not in y`
  - [ ] Conditional expression (`if cond: x elif cond: y else: z`)
  - [ ] Containers comprehensions (`for x in container expr(x)`)
  - [ ] Lambda expressions (`fun (x) => expr(x)`)
  - [ ] Pipe operator (`|>`)
  - [ ] Pattern matching (expr)
- Statements
  - [x] Variables/constants definitions (*no declaration w/out definition with a value!*)
    - [x] with type inference, if defined through value/constructor
    - [x] with explicit type declaration, if defined through expression or function call
  - [x] Variables assignment
  - [x] Loops
    - [x] Conditional loops: infinite, while, until, do..while, do..until
    - [ ] Container loop: `for x in y doSomething();` or `{ ... }`
  - [x] Conditional: if-elif-else
  - [ ] Pattern matching (stmnt)
- Types
  - [ ] Basic types
    - [x] Bool (`True` and `False`)
    - [ ] `None`
    - [ ] Number (one for int and float, with ext-functions, flags NoSign, NoFloat, NoComplex and so on..)
    - [ ] ComplexNumber
    - [ ] Generic containers (list, set, dict and so on..) with `<T>`
    - [ ] String (based on list of Unicode characters)
    - [ ] Functional type (in C turns to function pointer) (`T -> R` or `R(T)` ??)
  - [ ] Compound types
    - [ ] Product types (namedtuple/struct) (x * y)
    - [ ] Variant types (sum/union) (x | y)
    - [ ] Option type (x | None)
    - [ ] Intersection types (x & y) (at first, only for product types)
  - [ ] Type aliases
- Definitions
  - [x] Functions
  - [ ] Multiple function parameters (like in Python)
  - [ ] Function parameters with default values
  - [ ] Expression-returning functoins (`Number mul(x, y) = x * y;`)
  - [ ] Extension functions (`extend T: X func() { ... }`; also bunch of functions `extend T { ... X func() { ... } ... }`)
  - [ ] Modules/namespaces (?)
  - [ ] Bindings with C functions/libraries (not only C?)
- Other
  - [ ] IO standart functions
  - [ ] Multiple files compilation (as a project)
  - [ ] Pure functions boost (memoization or smth)
  - [ ] Multi-threading programming support
  - [ ] Coroutines and generators (?)
  - [ ] Monads (?)
