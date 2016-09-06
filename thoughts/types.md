## Types

### Variant types in Silver

- If a function takes an argument (or returnes a value) of variant type, the value in call (or in `return` statement) gets replaced by call of a function kind of:
```c
VariantTypeName* VariantTypeName__ObjectTypeName(ObjectTypeName arg)
```

The whole example:

**Silver**
```
type VariantTypeName =
    | First Type1
    | Second Type2;
def func1(arg: VariantTypeName) { ... }
let t = new Type2(...);
func1(First t);
def func2(...): VariantTypeName
{
    var tmp = new Type1(...);
    return Second tmp;
}
```

**C** (without modules names prefixes)
```c
struct VariantTypeName { ... };
struct VariantTypeName* VariantTypeName__Type1(Type1 arg) { ... };
struct VariantTypeName* VariantTypeName__Type2(Type2 arg) { ... };
void func1(struct VariantTypeName * arg) { ... }
const Type2 t = Type2__Constructor(...);
func1(VariantTypeName__Type2(t));
struct VariantTypeName* func2(...)
{
    Type1 tmp = Type1__Constructor(...);
    return VariantTypeName__Type1(tmp);
}
```

### Intersection types in Silver

...

### Interfaces in Silver

- Interfaces contain only functions.
- Interfaces can't have instances (objects).

```
interface iOpenable;

type Door =
    & iOpenable
    & ...;

type Book =
    & iOpenable
    & ...;

extend iOpenable
{
    open();
    close();
}

extend Door
{
    open() { ... }
    close() { ... }
    ...
}

extend Book
{
    open() { ... }
    close() { ... }
    ...
}

def openAndCloseSomething(smth: iOpenable)
{
    smth.open();
    smth.close();
}

def main()
{
    var myDoor = new Door(...);
    let myBook = new Book(...);

    openAndCloseSomething(myDoor);
    openAndCloseSomething(myBook);
}
```
