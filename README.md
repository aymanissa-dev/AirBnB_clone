# AirBnB Clone - The Console

## Description

This project is the first step towards building a full clone of the
[AirBnB](https://www.airbnb.com/) web application. It lays the foundation
for the entire stack: a command interpreter to manage the application's
objects, a base class that all future models inherit from, and a storage
engine that serializes objects to a JSON file so data survives between
program runs.

At this stage, the project provides:

- `BaseModel`: a parent class defining common attributes (`id`,
  `created_at`, `updated_at`) and methods (`save`, `to_dict`) shared by
  every future model (User, State, City, Place, etc.).
- `FileStorage`: an engine that serializes Python objects to a JSON file
  and deserializes them back into objects when the program restarts.

> **Status:** the command interpreter (`console.py`) described below is
> part of the next milestone and is not yet in this repository. The
> sections below document its intended usage so the interface is
> already specified before it's implemented.

Later steps will add the interactive command interpreter itself and the
remaining model classes.

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
help  quit

(hbnb) quit
$
```

It also supports non-interactive mode, so commands can be piped in:

```bash
$ echo "help" | ./console.py
(hbnb)
Documented commands (type help <topic>):
========================================
help  quit
(hbnb)
$
```

### Examples

```bash
$ ./console.py
(hbnb) quit
$
```

```bash
$ echo "quit" | ./console.py
(hbnb)
$
```

(More commands — `create`, `show`, `destroy`, `all`, `update` — will be
documented here as they are implemented.)

## Running the tests

```bash
$ python3 -m unittest discover tests
```

This also works in non-interactive mode:

```bash
$ echo "python3 -m unittest discover tests" | bash
```
