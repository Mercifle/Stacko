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
./Test.py
```

## Examples

### Hello, World!

```py
"Hello, world!" printLine
```

### Count Backwards From Ten

```py
10 dup 0 = not while {
    dup printLine   # Print counter value
    1 -             # Subtract one from counter
    dup 0 = not     # Check if counter is zero
}
```

## Language Reference

### Comments

All characters after the `#` symbol will be ignored by the interpreter until the beginning of the
next line. This feature can be used to include comments in code.

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

### Types

Values can fall into one of three types in Stack, those types being `number`, `boolean`, or `string`.
Three corresponding operators exist allowing you to *attempt* to convert a value of one type into that of another.
If the value you are trying to coerce cannot be coerced into the desired type, the program will crash.

#### Example

```py
"3.14" toNum  3.14   assertEqual
Yes toString  "Yes"  assertEqual
"Yes" toNum     # This line will cause the program to crash, as "Yes" cannot be converted to a number
```

### Operators

#### Stack Operations

| Name | Signature |   Description   |
|------|-----------|-----------------|
| dup | a -- a a | Duplicates the top-most value on the stack. |
| pop | a -- | Removes the top-most value from the stack. |

#### Arithmetic Operations

| Name | Signature |   Description   |
|------|-----------|-----------------|
| + | a b -- c | Adds two values on the top of the stack. |
| - | a b -- c | Subtracts two values on the top of the stack. |
| * | a b -- c | Multiplies two values on the top of the stack. |
| / | a b -- c | Divides two values on the top of the stack. |
| % | a b -- c | Performs modulo operatino on the two values on the top of the stack. |

#### Comparative Operations

| Name | Signature |   Description   |
|------|-----------|-----------------|
| = | a b -- c | Compares two values on top of the stack. |
| < | a b -- c | Applies the less than comparison to the two values on top of the stack. |
| <= | a b -- c | Applies the less than or equal to comparison to the two values on top of the stack. |
| > | a b -- c | Applies the greater than comparison to the two values on top of the stack. |
| >= | a b -- c | Applies the greater than or equal to comparison to the two values on top of the stack. |

#### Miscellaneous Operations

| Name | Signature |   Description   |
|------|-----------|-----------------|
| printLine | out -- | Writes the contents of a string to stdout, along with a trailing newline character. |
| readLine | -- in | Reads a single line of input from stdin, pushing the line's contents onto the value stack as a string. |
| exit | a -- | Exits with specified return code. |
| assert | a -- | Exits with return code of 1 if `a` is false. |
| assertEqual | a b -- | Exits with return code of 2 if both `a` and `b` are not equal. |
| assertNotEqual | a b -- | Exits with return code of 2 if both `a` and `b` equal. |

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


### Constants

Constants can be used to assign a name to a constant value of any type which can then later be referenced elsewhere in a script.

Constants can be created with the `const` keyword, followed by a name. Constants will be assigned the top-most value on the stack on definition, meaning that at least one value must already be on the stack before a constant can be defined.

#### Example

```py
# Create constant `pi` with the value 3.14
3.14 const pi
pi 3.14 assertEqual
```


### Variables

Variables can be used to assign a name to a value of any type which can then later be referenced elsewhere in a script. Unlike constants variables are mutable, meaning their contents can be modified after variable definition.

Variables in Stacko are loosely typed, meaning that the type of a given variable is not in any way enforced by the interpreter, and may be subject to change.

Variables can be created with the `var` keyword, followed by a name. Unlike constants, variables are not assigned a value upon initialization. Assigning a value to a variable is up to the user, and can be done with the `set` keyword, followed by the name of the variable you would like to modify. This will assign the selected variable with the top-most value on the stack.

#### Example

```py
# Define variable `foo`
var foo

# Assign `foo` a value of 3
3 set foo
foo 3 assertEqual

# Assign `foo` a value of "bar"
"bar" set foo
foo "bar" assertEqual
```


### Including Modules

Including external modules can be done using the `file` keyword, preceded by the path of the desired module relative to the main source file--that being the file which is initially passed to the Stacko interpreter to be run.

#### Example

```py
# Main.stko
file Defs.stko
file Lib/Math.stko

pi squared 9.8596 assertEqual
```

```py
# Defs.stko
3.14 const pi
```

```py
# Lib/Math.stko
fnn squared {
    toNum
    dup *
}