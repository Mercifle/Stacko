#!/usr/local/bin/python3
import sys
import re

### Error reporting
def reportError(msg):
    print(f"\33[31mError\33[0m: \33[32m{msg}\33[0m 😭", file=sys.stderr)

# TODO: Make sure a minimum of 2 arguments are passed
Path = sys.argv[1]

# Make sure file uses the '.stko' or '.stacko' extension
if not (Path.endswith(".stko") or Path.endswith(".stacko")):
    reportError("Extension was not '.stko' or '.stacko'")
    exit(1)

File = open(Path, "r")
Content = File.read()
File.close()

### Token parsing
Tokens = re.findall("(?:\".*?\"|\S)+", Content)

### Interpreting
def assertIdenticalTypes(a, b):
    if not (type(a) is type(b)):
        reportError(f"Type '{type(a).__name__}' and '{type(b).__name__}' cannot be used together in an operation.")
        exit(1)

Stack = []

for Token in Tokens:
    # Push string
    if Token.startswith('"') and Token.endswith('"'):
        Stack.append(Token[1:-1])

    # Push number
    elif Token.isdigit():
        NUMBER = int(Token)
        Stack.append(NUMBER)
    
    # Addition
    elif Token == "+":
        A = Stack.pop()
        B = Stack.pop()
        assertIdenticalTypes(A, B)

        RESULT = B + A
        Stack.append(RESULT)

    # Keyword 'println'
    elif Token == "println":
        print(Stack.pop())

    # Unknown token
    else:
        reportError(f"Unknown token '{Token}' found in '{Path}'.")
        exit(1)
