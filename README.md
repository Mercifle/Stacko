# Stacko

A simple stack-based programming language.

## Usage

### Run a Stacko script

**NOTE:** Stacko scripts **must** use either the `.stacko`, or `.stko` file extension.

```bash
./Stacko.py <script_path>
```

### Run Test Suite

```bash
python3 Test.py
```

## Examples

### Hello, World!

```py
"Hello, world!" printLine
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

| Name | Signature |   Description   |
|------|-----------|-----------------|
| printLine | out -- | Writes the contents of a string to stdout, along with a trailing newline character. |
| readLine | -- in | Reads a single line of input from stdin, pushing the line's contents onto the value stack as a string. |
| + | a b -- c | Adds two values on the top of the stack. |
| - | a b -- c | Subtracts two values on the top of the stack. |
| * | a b -- c | Multiplies two values on the top of the stack. |
| / | a b -- c | Divides two values on the top of the stack. |
| = | a b -- c | Compares two values on top of the stack. |
| not | a -- b | Performs a boolean not operation on the top-most value on the stack. |
| dup | a -- a a | Duplicates the top-most value on the stack. |

### Control Flow

If expressions can be used to execute code conditionally. If expressions begin with the `if` keyword
and are followed by an expression body--a sequence of instructions between a pair of curly braces.
If expressions may optionally be followed by an else expression.

If the top-most value on the stack when an if expression is encountered is true, the instructions
inside the if body will be executed. Otherwise, the following else expression will be run, if it
exists.

While expressions operate similarly to if expressions, except they will continually run the
instructions in their body so long as the value at the top of the stack is true.

#### Examples

##### If & Else Expressions

```py
No      # Pushes boolean `true` to the top of the stack
if {
    "This text will NOT be displayed." printLine
} else {
    "This text WILL be displayed." printLine
}
```

##### While Expression

```py
# Count downwards from 10
10 dup 0 = not while {
    dup printLine
    1 -
    dup 0 = not
}
```

### Functions

Functions can be used to reuse code multiple times within a script easily.

Functions can be created by using the `fnn` keyword, followed by a name and a body.

#### Example

```py
fnn sayHello {
    "Hello, "   print
                print
    "!"         printLine
}

"World" sayHello    # Prints "Hello, World!"
```

### Type Casting

Values can be cast between types by means of a few select keywords, namely `toNum`, `toString`, and
`toBool`.

#### Example

```py
"3.14" toNum
2 *
printLine   # Prints 6.28

"No" toBool not
printLine   # Prints Yes
```

