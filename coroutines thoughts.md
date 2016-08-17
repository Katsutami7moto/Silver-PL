## Coroutines

### Example on Python

```python
def calc():
    history = []
    while True:
        x, y = (yield)
        if x == 'h':
            print history
            continue
        result = x + y
        print result
        history.append(result)

c = calc()

print type(c) # <type 'generator'>

c.next() # Необходимая инициация. Можно написать c.send(None)
c.send((1,2)) # Выведет 3
c.send((100, 30)) # Выведет 130
c.send((666, 0)) # Выведет 666
c.send(('h',0)) # Выведет [3, 130, 666]
c.close() # Закрывем генератор
```

### Trying to make this in Silver with module (no generator objects, no prepared methods, but easier usage)

```
module crtn
{
    var history = new List();
    def calc(x: int = 0, y: int = 0)
    {
        if x == 0 and y == 0 { history.print(); }
        else
        {
            var result: int = x + y;
            result.print();
            history.append(result);
        }
    }
    def close() { history.empty(); }
}

module main
{
    import crtn;
    def main()
    {
        calc(1, 2);
        calc(100, 30);
        calc(666, 0);
        calc();
        close();
    }
}
```

### The same in Silver with type and extension functions (posible to create objects)

```
module crtn
{
    type calcable = history: List;
    extend calcable
    {
        def calc(x: int = 0, y: int = 0)
        {
            if x == 0 and y == 0 { self.history.print(); }
            else
            {
                var result: int = x + y;
                result.print();
                self.history.append(result);
            }
        }
        def close() { self.history.empty(); }
    }
}

module main
{
    import crtn;
    def main()
    {
        c = new calcable([]);
        c.calc(1, 2);
        c.calc(100, 30);
        c.calc(666, 0);
        c.calc();
        c.close();
    }
}
```

### Wikipedia example

```
var q := new queue

coroutine produce
    loop
        while q is not full
            create some new items
            add the items to q
        yield to consume
        summarize

coroutine consume
    loop
        while q is not empty
            remove some items from q
            use the items
        yield to produce
        analyse
```

### Silver

```

```

### Generator on Python

```python
def numbers(x):
    for i in range(x):
        if i % 2 == 0:
            yield i

for n in numbers(11):
    print n
```

### Silver

```
gen numbers(x: int): int
{
    for i in range(x) { if i % 2 == 0 { yield i; } }
}

for n in numbers(11) { n.print(); }
```

### Translates in C as

Use this: http://club.shelek.ru/viewart.php?id=338 

```c
int numbers(ccrContParam, int x) {
    ccrBeginContext;
    int i;
    ccrEndContext(foo);

    ccrBegin(foo);
    for (foo->i=0; foo->i<x; foo->i++) {
       if ((i % 2) == 0) { ccrReturn(foo->i); }
    }
    ccrFinish(-1);
}

void main(void) {
   ccrContext z = 0;
   do {
      printf("%d\n", ascending(&z, 11));
   } while (z);
}
```
