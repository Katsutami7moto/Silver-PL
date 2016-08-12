# Code examples

## Variables/constants declaration

If the type of variable/constant is obvious (rvalue is a basic type literal or a compound type constructor), then you don't need explicit type declaration, just `var x = ...;`.
If rvalue is a function call or any kind of expression, then the type should be declared: `var x : Type = ...;`.

### Silver

```
var x : int = fib(8);
var xx : double = 8 / 9;
var y = 5;

let s : String = concat("Hello, ", "World!");
let zz : Bool = 3 - 4 >= 9 % 7 + 2;
let z = 9.8;
```

### Translates in C as

```c
int x = fib(8);
double xx = (8.0 / 9.0);
int y = 5;

const String s = concat("Hello, ", "World!");
const int zz = ((3 - 4) >= ((9 % 7) + 2));
const double z = 9.8;
```

## Expression-functions

### Silver

```
def sum(x: int, y: int): int => x + y;

def fib(n: int): int => if n == 0 or n == 1: n elif n > 1: fib(n-1) + fib(n-2) else: (-1)**(1-n) * fib(-n);
```

### Translates in C as

```c
int sum(int x, int y) { return x + y; }

int fib(int n) { if ((n == 0) || (n == 1)) { return n; } else if (n > 1) { return fib(n-1) + fib(n-2); } else { return power((-1), (1-n))*fib(-n); } }
```

## Modules

Importing and using modules are intransitive, so there won't be errors of recursive using (so, yeah, you won't be stopped from recursion like in example below), but, if you want to use a module 'clearly', you should have a 'reload' function in it.

### Silver

```
module Fisrt
{
def foo() { ... Third::fuba(); ... }
}

module Second
{
def bar() { ... First::foo(); ... }
}

module Third
{
import First;
import Second;

def fuba() { ... foo(); ... bar(); ... }
}
```

### Translates in C as

```c
void First__foo();

void Third__fuba();

void First__foo() { ... Third__fuba(); ... }

void Second__bar();

void Second__bar() { ... First__foo(); ... }

void Third__fuba() { ... First__foo(); ... Second__bar(); ... }
```
