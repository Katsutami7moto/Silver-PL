# Silver
Silver is general-purpose programming language, which goal is to collect many useful features from other languages, but avoid their design and working errors.

## Concepts

- Functional programming features: anonymous functions, first-class functions, closures
- Compound types, interfaces and extension functions will make code more familiar to OOP-users
- No automatic/implicit type conversion, static strong type system
- Statement-based language, not expression-based
- No low-level looking basic types like `uint32` (only `int` and `double` for trivial tasks)
- Silver compiler translates code to C language (C89 standart) for good portabilty and performance
- The core of Silver will be preserved after the full completion of its design - none of next updates will break compatibility! And compatibility won't impede the further development (as it won't affect the core)

## Features

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
    - [ ] Containers comprehensions (`[for x in container: expr(x)]`)
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
        - [ ] Container loop: `for x in container { ... }`
    - [x] Conditional: if-elif-else
    - [ ] Pattern matching (stmnt)
- Types
    - [ ] Basic types
        - [x] bool (`True` and `False` -> `0` and `1` in C)
        - [x] int
        - [x] double
        - [ ] char (Unicode)
        - [ ] Сontainers with generics
            - [ ] `List<T>` (double-linked list, indexed, with all elements of type T)
            - [ ] `Set<T>` (unordered set, with all elements (no duplicates) of type T)
            - [ ] `Dict<K, T>` (associative array, with all keys (no duplicates) of type K and all elements of type T)
            - [ ] ...
        - [ ] String (based on List of Unicode characters)
        - [ ] `None`
        - [ ] Functional type `(T): R` (in C turns to function pointer)
        - [ ] BigNum (list based, one for int and float, with ext-functions, flags NoSign, NoFloat, NoComplex and so on..)
        - [ ] ComplexNum
    - [ ] Compound types
        - [ ] Product types (namedtuple/struct) (* x * y ...) (made of any types)
            - [ ] With generics `<T>`
        - [ ] Intersection types (& x & y ...) (made of product types without equal-named fields) (rename it into 'conjunction type' or smth??)
            - [ ] With generics `<T>`
        - [ ] Variant types (sum/tagged union) (| x | y ...) (made of any types) (http://en.wikipedia.org/wiki/Tagged_union)
            - [ ] With generics `<T>`
            - [ ] `type Option<T> = T | None;` (??)
        - [ ] Interfaces (variant types with extension functions)
            - [ ] With generics `<T>` (??)
    - [ ] Type aliases (`typedef`)
        - [ ] With generics `<T>` (??)
    - [ ] Loading types from C
- Definitions
    - [x] Functions
    - [ ] Modules (to group functions and some external variables/constants for them)
    - [ ] Extension functions (`extend Type: func() { ... }`; also bunch of functions `extend Type { func() { ... } ... }`)
        - [ ] For product types
        - [ ] For intersection types
    - [ ] Expression-returning functions (`def sum(x: int, y: int): int => x + y;`)
    - [ ] Multiple and keyword function parameters (like in Python)
    - [ ] Function parameters with default values (like in Python)
    - [ ] Bindings with C functions/libraries (not only C?)
- Other
    - [ ] IO standart functions
    - [ ] Multiple files compilation (as a project)
    - [ ] Pure functions boost (memoization or smth)
    - [ ] Multi-threading programming support (?)
    - [ ] Coroutines and generators (?)
    - [ ] Monads (?)
