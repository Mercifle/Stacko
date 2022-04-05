# Stacko

A simple stack-based programming language.

## Usage

### Run a Stacko script

**NOTE:** Stacko scripts **must** use either the `.stacko`, or `.stko` file extension.

```bash
./Stacko.py <script_path>
```

## Examples

### Hello, World!

```py
"Hello, world!" println
```

## Language Reference

### Comments

All characters after the `#` symbol will be ignored by the interpreter until the beginning of the
proceeding line. This feature can be used to include comments in code.

#### Example
```py
# This is a comment. This text will be ignored by the interpreter.
```

### Literals

When encountered by the interpreter, literal values are appended to the top of the value stack for
later use.

#### Example

```py
"Hello, world!"     # Pushes string literal `Hello, world!`
3.14                # Pushes number literal `3.14`
Yes                 # Pushes boolean literal `true`
No                  # Pushes boolean literal `false`
```

### Keywords

|   Name   |   Description   |
|----------|-----------------|
| println  | Writes the string at the top of the value stack to stdout, along with a trailing newline. |
|    +     | Takes the two top-most values on the stack, adds their values together, then pushes the result to the top of the stack. |
|    -     | Subtracts the value of the top-most value on the stack from the value below it, then pushes the result to the top of the stack. |
|    *     | Multiplies the two top-most values on the stack with one another, then pushes the result to the top of the stack. |
|    /     | Divides the value of the second to top-most value on the stack by the value above it, then pushes the result to the top of the stack. |
|    =     | Compares the two top-most values on the stack, pushing `Yes` to to top of the stack if they are equal, pushing `No` otherwise. |
|   not    | Performs a boolean not operation on the top-most value on the stack. |

### Control Flow

If expressions can be used to execute code conditionally. If expressions begin with the `if` keyword
and are followed by an expression body--a sequence of instructions between a pair of curly braces.

If the top-most value on the stack when an if expression is encountered is true, the instructions
inside the if body will be executed. Otherwise, they will be ignored.

#### Example

```py
Yes     # Pushes boolean `true` to the top of the stack
if {
    "This text will be displayed." printLine
}

No      # Pushes boolean `false` to the top of the stack
if {
    "This text will NOT be displayed." printLine
}
```
