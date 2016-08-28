## Functional programming

Concepts:

### Functions are first-class objects

You may assign functions as rvalue

**Silver**
```
def foo(a: Type1, b: Type2): Type3 { ... }
var x: (Type1, Type2): Type3 = foo;
let y: Type3 = x(...);
typedef Ftype = (Type1, Type2): Type3;
let bar: Ftype = x;
var z: Type3 = bar(...);
```

**C**
```c
Type3 foo(Type1 a, Type2 b) { ... }
Type3 (*x)(Type1, Type2) = foo;
const Type3 y = x(...);
Type3 (*bar)(Type1, Type2) = x;
Type3 z = bar(...);
```

You may take functions as arguments of other functions

**Silver**
```
def map(x: IntList, f: (int): int): IntList { ... }
def foo(x: int): int { ... }
var list2: IntList = map(list1, foo);
```

**C**
```c
IntList map(IntList x, int (*f)(int)) { ... }
int foo(int x) { ... }
IntList list2 = map(list1, foo);
```

You may return functions from other functions

**Silver**
```
def foo(x: int): int { ... }
def bar(x: int): int { ... }
def choose(a: bool): (int): int { if a { return foo; } else { return bar; } }
var Tfoo: (int): int = choose(5 > 4);
let foot: int = Tfoo(9);
```

**C**
```c
int foo(int x) { ... }
int bar(int x) { ... }
int (*choose(int a))(int) { if (a) { return foo; } else { return bar; } }
int (*Tfoo)(int) = choose(5 > 4);
const int foot = Tfoo(9);
```

### Closure, currying and partial application

https://ru.wikibooks.org/wiki/%D0%A0%D0%B5%D0%B0%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%B8_%D0%B0%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC%D0%BE%D0%B2/%D0%97%D0%B0%D0%BC%D1%8B%D0%BA%D0%B0%D0%BD%D0%B8%D0%B5#Python

**Silver**

Nested function example
```
def funky(a: int): (int): double
{
    ...
}
```

Lambda example
```
let sum3 = fun (x: int) => fun (y: int) => fun (z: int) => x + y + z;
let addThree = sum3(3);
let addSeven = addThree(4);
let Twelve = addSeven(5);
let Thirteen = sum3(4, 2, 7);
```

**C**

Nested function example
```c

```

Lambda example
```c

```

### Pure functions boost

Memoization by saving arguments (in tuple) and results in pairs into a special dictionary (named "modulename__funcname__sanctuary") and cheking them inside the pure function (added automatically).

You define pure functions by keyword `pure`.
In pure functions you can't:
    - Use/modify module fields or any fieds from outside scopes
    - Modify function arguments
    - Call unpure functions
    - Return unpure functions
    - Do IO operations
    - Not to return a value
    - Not to take values
