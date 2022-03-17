# Stacko

A simple stack-based programming language.

## Usage

### Run a Stacko script

**NOTE:** Stacko scripts **must** use either the `.stacko`, or `.stko` file extension.

```py
./Stacko.py <script_path>
```

## Examples

### Hello, World!

```py
"Hello, world!" println
```

## Language Reference

### Literals

When encountered by the interpreter, literal values are appended to the top of the value stack for
later use.

#### Examples

This program pushes the string literal `Hello, world!`, and the number literal `42` to the top of the value stack.

```py
"Hello, world!" 42
```

### Keywords

|   Name   |   Description   |
|----------|-----------------|
| println  | Writes the string at the top of the value stack to stdout, along with a trailing newline. |
|----------|-----------------|
|    +     | Takes the two top-most values on the stack, adds their values together, then pushes the result to the top of the stack. |
