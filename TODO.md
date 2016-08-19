## TODO

- [x] Fix issue #4
- [ ] Fix issue #2
- [ ] Fix issue #1
- [ ] Modules (statements `module` and `import`, with correct placing of declarations and realizations)
- [ ] Nested modules
- [ ] Appeal to nested modules/fields through dots
- [ ] Product types, their constructors and destructors (`del` statement)
- [ ] Extension functions
- [ ] Product types with generics (use `<T>` or `[T]` ??)
- [ ] List literals
- [ ] List type, basic fucntions and behavior (`[x..y..z], list[i], list[a:b]`; List.append and others..)
- [ ] `for` loop
- [ ] Conditions `in`/`not in`, using in `if` and loops
- [ ] List comprehensions
- [ ] Char literals
- [ ] `char` type (UTF-8 !!)
- [ ] `typedef`
- [ ] String literals
- [ ] `String` type (`typedef String = List<char>;` or like that)
- [ ] ...

### Where is symbol table needed (according to silv_parser):

- In checking the type of element/expression (getting type of ident-element);
- In atom parsing (external var);
- In expression parsing (making function call Token);
- In var/let parsing (checking written and writing new ones);
- In mod parsing (checking if present, if var, and proper rvalue type checking);
- In func parsing (checking written and writing new ones);
