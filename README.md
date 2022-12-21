# Stacko

A simple stack-based programming language.

## Usage

### Run a Stacko script

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

## Documentation

See the [official Stacko docs](https://suirabu.github.io/stacko-docs/).

