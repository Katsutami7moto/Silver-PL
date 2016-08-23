## Functional programming

Concepts:

### Functions are first-class objects

#### You may assign functions as rvalue

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

#### You may take functions as arguments of other functions

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

#### You may return functions from other functions

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

#### Closure, currying and partial application

**Silver**
```
let sum3 = fun (x: int) => fun (y: int) => fun (z: int) => x + y + z;
let addThree = sum3(3);
let addSeven = addThree(4);
let Twelve = addSeven(5);
let Thirteen = sum3(4, 2, 7);
```

**C**
```c

```
