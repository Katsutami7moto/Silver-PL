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
// typedef M<T> = T -> T;
// "!" marks a function with closure
let mul = fun : Number!  
(x) => fun : M<Number>
(y) => x * y;

mul : Number, Number -> Number
(x, y) => x * y;

// syntax
// funcname or "fun" : signature (arglist) => expr;
// funcname or "fun" [: signature] ([arglist]) { ... };

sqr : M<Number>
(x) => x * x;

fib : M<Number>
(n) =>  if n == 0 or n == 1: n
        elif n > 1: fib(n-1) + fib(n-2)
        else: (-1)**(1-n) * fib(-n);
```
