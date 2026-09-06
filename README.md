# AirBnB Clone - The Console

## Description

This project is the first step towards building a full clone of the
[AirBnB](https://www.airbnb.com/) web application. It implements the
foundation for the entire stack: a command interpreter to manage the
application's objects, a base class that all model classes inherit
from, and a storage engine that serializes objects to a JSON file so
data survives between program runs.

The project currently provides:

- `BaseModel`: a parent class defining common attributes (`id`,
  `created_at`, `updated_at`) and methods (`save`, `to_dict`) shared by
  every model.
- Model classes `User`, `State`, `City`, `Amenity`, `Place`, and
  `Review`, each inheriting from `BaseModel` and adding the attributes
  relevant to that object.
- `FileStorage`: an engine that serializes Python objects to a JSON
  file and deserializes them back into objects when the program
  restarts.
- `console.py`: an interactive command interpreter for creating,
  inspecting, updating, and deleting these objects.

## The Command Interpreter

The command interpreter is a custom shell (built with Python's `cmd`
module) used to create, update, destroy, and manage the objects of this
project without needing a web interface.

### How to start it

Make the console executable and run it directly, or invoke it with
Python:

```bash
$ ./console.py
```

or

```bash
$ python3 console.py
```

### How to use it

Once started, you'll see a `(hbnb)` prompt waiting for a command:

```
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  emptyline  help  quit  show  update

(hbnb) quit
$
```

It also supports non-interactive mode, so commands can be piped in:

```bash
$ echo "help" | ./console.py
```

### Supported commands

| Command   | Usage                                              | Description                                    |
|-----------|-----------------------------------------------------|-------------------------------------------------|
| `create`  | `create <class name>`                                | Creates a new instance, saves it, prints its id  |
| `show`    | `show <class name> <id>`                             | Prints the string representation of an instance  |
| `destroy` | `destroy <class name> <id>`                          | Deletes an instance                              |
| `all`     | `all [<class name>]`                                 | Prints all instances, optionally filtered        |
| `count`   | `count <class name>`                                 | Prints the number of instances of a class        |
| `update`  | `update <class name> <id> <attribute> "<value>"`     | Updates (or adds) an attribute on an instance     |
| `quit` / `EOF` | `quit`                                          | Exits the console                                |

Every command also supports the alternative `<class name>.<command>(<args>)`
syntax, e.g. `User.all()`, `User.count()`, `User.show("<id>")`,
`User.destroy("<id>")`, `User.update("<id>", "<attribute>", "<value>")`,
or `User.update("<id>", {"<attribute>": "<value>", ...})` to update
several attributes at once.

Valid class names: `BaseModel`, `User`, `State`, `City`, `Amenity`,
`Place`, `Review`.

### Examples

```bash
$ ./console.py
(hbnb) create User
49faff9a-6318-451f-87b6-910505c55907
(hbnb) show User 49faff9a-6318-451f-87b6-910505c55907
[User] (49faff9a-6318-451f-87b6-910505c55907) {'id': '49faff9a-...', ...}
(hbnb) User.update("49faff9a-6318-451f-87b6-910505c55907", "first_name", "Betty")
(hbnb) User.count()
1
(hbnb) destroy User 49faff9a-6318-451f-87b6-910505c55907
(hbnb) quit
$
```

```bash
$ echo "create BaseModel" | ./console.py
(hbnb) 3aa5babc-9d1d-4b7e-b779-3b092b4657f9
(hbnb)
$
```

## Running the tests

```bash
$ python3 -m unittest discover tests
```

This also works in non-interactive mode:

```bash
$ echo "python3 -m unittest discover tests" | bash
```
