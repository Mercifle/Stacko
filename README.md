# Stacko

A simple stack-based programming language.

## Usage

Run a Stacko script

**NOTE:** Stacko scripts **must** use either the `.stacko`, or `.stko` file extension.

```
./Stacko.py <script_path>
```

## Examples

Hello, World!

```py
"Hello, world!" println
```

## Language Reference

### Literals

When encountered by the interpreter, literal values are appended to the top of the value stack for
later use.

#### Examples

This program pushes the values `Hello, ` and `world!` to the top of the value stack.

```
"Hello, "
"world!"
```

### Keywords

|   Name   |   Description   |
|----------|-----------------|
| println  | Writes the string at the top of the value stack to stdout, along with a trailing newline. |

