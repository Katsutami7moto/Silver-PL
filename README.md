# Silver
Silver is general-purpose programming language, which goal is to collect many useful features from other languages, but avoid their design and working errors.

## Concepts

- Functional programming features: anonymous functions, first-class functions, closures, currying, partial application, orientation on programminng w/out variables
- Compound types and extension functions will make code more familiar to OOP-users
- No automatical/implicit type conversion, static strong type system
- Statement-based language, not expression-based
- No low-level looking basic types like `uint32` (only `int` and `double` for trivial tasks)
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
  - [ ] Containers comprehensions (`for x in container: expr(x)`)
  - [ ] Lambda expressions (`fun (x) => expr(x)`)
  - [ ] Pipe operator (`|>`)
  - [ ] Pattern matching (expr)
- Statements
  - [x] Variables/constants definitions (**no declaration w/out definition with a value!**)
    - [x] with type inference, if defined through value/constructor `var/let x = ...;`
    - [x] with explicit type declaration, if defined through expression or function call `var/let x : Type = ...;`
  - [x] Variables assignment (also augmented) `mod x = ...;`
  - [x] Loops
    - [x] Conditional loops: infinite, while, until, do..while, do..until
    - [ ] Container loop: `for x in container doSomething();` or `for x in container { ... }`
  - [x] Conditional: if-elif-else
  - [ ] Pattern matching (stmnt)
- Types
  - [ ] Basic types
    - [x] Bool (`True` and `False` -> `0` and `1` in C)
    - [x] int
    - [x] double
    - [ ] Сontainers with generics `<T>`
      - [ ] List
      - [ ] Set
      - [ ] Dict
      - [ ] Tuple
      - [ ] ...
    - [ ] String (based on list of Unicode characters)
    - [ ] Functional type (in C turns to function pointer) (`T -> R` or `R(T)` ??)
    - [ ] RealNum (list based, one for int and float, with ext-functions, flags NoSign, NoFloat, NoComplex and so on..)
    - [ ] ComplexNum
    - [ ] `None`
  - [ ] Compound types
    - [ ] Product types (namedtuple/struct) (x * y)
      - [ ] With generics `<T>`
    - [ ] Variant types (sum/union) (x | y)
    - [ ] Option type (x | None)
    - [ ] Intersection types (x & y) (at first, only for product types)
  - [ ] Type aliases
  - [ ] Loading types from C
- Definitions
  - [x] Functions
  - [ ] Multiple function parameters (like in Python)
  - [ ] Function parameters with default values
  - [ ] Expression-returning functoins (`def sum(x: int, y: int): int => x + y;`)
  - [ ] Extension functions (`extend Type: func() { ... }`; also bunch of functions `extend Type { def func() { ... } ... }`)
  - [ ] Modules/namespaces (?)
  - [ ] Bindings with C functions/libraries (not only C?)
- Other
  - [ ] IO standart functions
  - [ ] Multiple files compilation (as a project)
  - [ ] Pure functions boost (memoization or smth)
  - [ ] Multi-threading programming support
  - [ ] Coroutines and generators (?)
  - [ ] Monads (?)

## Actual TODO

- [ ] Fix issue #4
- [ ] Fix issue #2
- [ ] Fix issue #1
- [ ] Product types, their constructors and destructors (`del` statement)
- [ ] Extension functions
- [ ] Product types with generics `<T>`
- [ ] List literals
- [ ] List type, basic fucntions and behavior (`[x..y..z], list[i], list[a:b]`; List.append and others..)
- [ ] `for` loop
- [ ] Conditions `in`/`not in`, using in `if` and loops
- [ ] List comprehensions
- [ ] String literals
- [ ] `String` type and all its functions/behavior
- [ ] ...
