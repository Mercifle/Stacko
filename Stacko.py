#!/usr/bin/python3
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
<<<<<<< Updated upstream
=======
Tokens.reverse()

def generateBlocksFromTokens():
    Block = []

    while len(Tokens) > 0 and Tokens[-1] != "}":
        Token = Tokens.pop()

        if Token == "if":
            assert(Tokens.pop() == "{")
            Block.append((Token, [generateBlocksFromTokens()]))
            assert(Tokens.pop() == "}")

            if len(Tokens) != 0 and Tokens[-1] == "else":
                Tokens.pop() # Pop 'else' token

                assert(Tokens.pop() == "{")
                Block[-1][1].append(generateBlocksFromTokens())
                assert(Tokens.pop() == "}")
        else:
            Block.append((Token, None))
    
    return Block

Blocks = generateBlocksFromTokens()
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
    # Push number
    elif Token.isdigit():
        NUMBER = int(Token)
        Stack.append(NUMBER)
    
    # Addition
    elif Token == "+":
        assertMinStackSize(2)
        A = Stack.pop()
        B = Stack.pop()
        assertIdenticalTypes(A, B)

        RESULT = B + A
        Stack.append(RESULT)

    # Keyword 'println'
    elif Token == "println":
        assertMinStackSize(1)
        print(Stack.pop())

    # Unknown token
    else:
        reportError(f"Unknown token '{Token}' found in '{Path}'.")
        exit(1)
=======
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
        
        # Equality
        elif Token == "=":
            assertMinStackSize(2)
            A = Stack.pop()
            B = Stack.pop()
            assertIdenticalTypes(A, B)

            RESULT = (B == A)
            Stack.append(RESULT)

        # Equality
        elif Token == "not":
            assertMinStackSize(1)
            COND = Stack.pop()
            assertType(COND, bool)

            Stack.append(not COND)

        # Keyword 'printLine'
        elif Token == "printLine":
            assertMinStackSize(1)
            printValue(Stack.pop())

        # Keyword 'if'
        elif Token == "if":
            assertMinStackSize(1)
            COND = Stack.pop()
            assertType(COND, bool)

            if COND == True:
                interpretBlocks(Block[0])
            elif len(Block) == 2:
                interpretBlocks(Block[1])

        # Unknown token
        else:
            reportError(f"Unknown token '{Token}' found in '{Path}'.")
            exit(1)

interpretBlocks(Blocks)
>>>>>>> Stashed changes
