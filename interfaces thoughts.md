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

- Interface contains only functions.
- Interface can't have instances (objects).
- Interface can't be a return type of a function.
- You describe what types are suitable for these interfaces instead of what interfaces implement these types.
- Same type can suit to many interfaces.
- You may add new type suiting to some interface when and where you want it.
- You may extend interfaces wtih new function prototypes when and where you want it.
- If function takes an interface argument, it compiles in several functions with different arguments in its place. (or use macro?)
- The interface itself isn't presented in generated code.

```
interface iOpenable
{
    open();
    close();
}

extend iOpenable: some_func(some_item: some_type): some_type;

suit iOpenable: Door, Book;

type Door = ... ;
extend Door
{
    open() { ... }
    close() { ... }
    some_func(some_item: some_type): some_type { ... }
    ...
}

type Book = ... ;
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
    var myBook = new Book(...);

    openAndCloseSomething(myDoor);
    openAndCloseSomething(myBook);
}
```
