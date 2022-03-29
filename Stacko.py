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

def assertMinStackSize(minSize):
    if len(Stack) < minSize:
        reportError(f"Expected at least {minSize} item(s) on stack to perform operation. Found {len(Stack)} instead.")
        exit(1)

for Token in Tokens:
    # Push string
    if Token.startswith('"') and Token.endswith('"'):
        Stack.append(Token[1:-1])

    # Push number
    elif Token.lstrip("-+").replace(".", "", 1).isdigit():
        NUMBER = float(Token)
        Stack.append(NUMBER)
    
    # Push 'Yes'
    elif Token == "Yes":
        Stack.append(True)

    elif Token == "No":
        Stack.append(False)

    ### Arithmetic operations

    # Addition
    elif Token == "+":
        assertMinStackSize(2)
        A = Stack.pop()
        B = Stack.pop()
        assertIdenticalTypes(A, B)

        RESULT = B + A
        Stack.append(RESULT)

    # Subtraction
    elif Token == "-":
        assertMinStackSize(2)
        A = Stack.pop()
        B = Stack.pop()
        assertIdenticalTypes(A, B)

        RESULT = B - A
        Stack.append(RESULT)
    
    # Multiplication
    elif Token == "*":
        assertMinStackSize(2)
        A = Stack.pop()
        B = Stack.pop()
        assertIdenticalTypes(A, B)

        RESULT = B * A
        Stack.append(RESULT)

    # Division
    elif Token == "/":
        assertMinStackSize(2)
        A = Stack.pop()
        B = Stack.pop()
        assertIdenticalTypes(A, B)

        RESULT = B / A
        Stack.append(RESULT)

    # Keyword 'PrintLine'
    elif Token == "PrintLine":
        assertMinStackSize(1)
        print(Stack.pop())

    # Unknown token
    else:
        reportError(f"Unknown token '{Token}' found in '{Path}'.")
        exit(1)
