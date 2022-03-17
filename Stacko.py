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
Stack = []

for Token in Tokens:
    # Push string
    if Token.startswith('"') and Token.endswith('"'):
        Stack.append(Token[1:-1])

    # Keyword 'println'
    elif Token == "println":
        print(Stack.pop())

    # Unknown token
    else:
        reportError(f"Unknown token '{Token}' found in '{Path}'.")