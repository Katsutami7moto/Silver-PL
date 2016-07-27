## Variables/constants declaration

```
var x : Number = fib(8);
var xx : Number = 8 / 9;
var y = 5;

let s : String = concat("Hello, ", "World!");
let zz : Bool = 3 - 4 >= 9 % 7 + 2;
let z = 9.8;
```

## Expression-functions

```
def sum(x: int, y: int): int => x + y;

let sum = fun (x: int)! => fun (y: int): int => x + y;

def fib(n: int): int => if n == 0 or n == 1: n elif n > 1: fib(n-1) + fib(n-2) else: (-1)**(1-n) * fib(-n);
```
