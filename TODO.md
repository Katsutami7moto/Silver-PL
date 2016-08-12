## TODO

- [x] Fix issue #4
- [ ] Fix issue #2
- [ ] Fix issue #1
- [ ] Modules (statements `module` and `import`, with correct placing of declarations and realizations)
    1. Divide all tokens to [ ['module', ...], ['module', ...], ... ]
    2. While/after dividing, get all modules names and write them to symbol table
    3. In a module:
        - Make a Module object with its name
        - Divide all module tokens to [ [kw, ...], [kw, ...], ... ], where kw is in { Use | Import | Type | Typedef | VarB | LetB | Extend | Def } (in that order they will appear in Module object)
        - Parse all nested lists:
            1. Fill the uses part
            2. Fill the declarations part (vars, consts and funcs have separate declaraions; so their lists shall be moved for further definitions parsing)
            3. Fill the definitions part
- [ ] Product types, their constructors and destructors (`del` statement)
- [ ] Extension functions
- [ ] Product types with generics `<T>` (use `<T>` or `[T]` ??)
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
