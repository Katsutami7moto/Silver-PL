## Interfaces

### Example in C++:

(interface is an abstract class with only abstract methods (virtual and without realization in interface itself))

```cpp
class iOpenable
{
    public:
    virtual ~iOpenable(){}
    virtual void open()=0;
    virtual void close()=0;
};

class Door: public iOpenable
{
    public:
    Door(){std::cout << "Door object created" << std::endl;}
    virtual ~Door(){}
    // Concretization of interface iOpenable methods for Door class
    virtual void open(){std::cout << "Door opened" << std::endl;}
    virtual void close(){std::cout << "Door closed" << std::endl;}
    // Method and fields that are specific for Door class
    // ...
};

class Book: public iOpenable
{
    public:
    Book(){std::cout << "Book object created" << std::endl;}
    virtual ~Book(){}
    // Concretization of interface iOpenable methods for Book class
    virtual void open(){std::cout << "Book opened" << std::endl;}
    virtual void close(){std::cout << "Book closed" << std::endl;}
    // Method and fields that are specific for Book class
    // ...
};

void openAndCloseSomething(iOpenable& smth)
{
    smth.open();
    smth.close();
}

int main()
{
    Door myDoor;
    Book myBook;

    openAndCloseSomething(myDoor);
    openAndCloseSomething(myBook);
    system ("pause");
    return 0;
}
```

### How to make this in Silver

- Variant type can't have his own methods like product and intersection types can, because this would lead to uncomfortable syntax.
- So, interfaces are only way to create variant types with unified methods (and also, of course, to make OOP-like interfaces and abstract classes).
- Using the interface automatically creates a variant type with its name (in compiled code remains the one structure).
- If a function takes an argument (or returnes a value) of variant/interface type, the value in call (or in `return` statement) gets replaced by call of a function kind of:
```c
VariantTypeName* VariantTypeName__ObjectTypeName(ObjectTypeName arg)
```

The whole example:

**Silver**
```
type VariantTypeName = Type1 | Type2;
def func1(arg: VariantTypeName) { ... }
let t = new Type2(...);
func1(t);
def func2(): VariantTypeName
{
    var tmp = new Type1(...);
    return tmp;
}
```

**C** (without modules names prefixes)
```c
struct VariantTypeName { ... };
struct VariantTypeName* VariantTypeName__Type1(Type1 arg);
struct VariantTypeName* VariantTypeName__Type2(Type2 arg);
void func1(struct VariantTypeName * arg) { ... }
const Type2 t = Type2__Constructor(...);
func1(VariantTypeName__Type2(t));
struct VariantTypeName* func2()
{
    Type1 tmp = Type1__Constructor(...);
    return VariantTypeName__Type1(tmp);
}
```

- Interfaces contain only functions.
- Interfaces can't have instances (objects).
- You describe what types are suitable for these interfaces instead of what interfaces implement these types.
- Same type can suit to many interfaces.

- You may add new type suiting to some interface when and where you want it.
- You may extend interfaces wtih new function prototypes when and where you want it.
- Any of these two operations in your module done to the interface from another module creates a copy of this interface in your module. (or make a special operation to copy types?)

```
type Door = ... ;
type Book = ... ;

interface iOpenable
{
    open();
    close();
}

extend iOpenable: some_func(some_item: some_type): some_type;

suit iOpenable: Door, Book;

extend Door
{
    open() { ... }
    close() { ... }
    some_func(some_item: some_type): some_type { ... }
    ...
}

extend Book
{
    open() { ... }
    close() { ... }
    some_func(some_item: some_type): some_type { ... }
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
