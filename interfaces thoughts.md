## Interfaces

### Example in C++ (interface is an abstract class with only abstract methods (virtual and without realization in interface itself)):

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

Interfaces contain only functions.
Interfaces can't have instances (objects).
You describe what types are suitable for this interface instead of what interface implements this type.
You may add new type suiting to some interface when and where you want it.
You may extend interfaces wtih new function prototypes when and where you want it.
Suiting types are absolutely normal Silver types.
If function takes an interface argument, it compiles in several functions with different arguments in its place. (or use macro?)
The interface itself isn't presented in generated code.

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
