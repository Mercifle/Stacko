#!/usr/bin/env python3
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
ContentLines = File.readlines()
File.close()

### Token parsing
Tokens = []

# Collect tokens, discarding tokens after the '#' symbol (comments)
for Line in ContentLines:
    LineTokens = re.findall("(?:\".*?\"|\S)+", Line)
    for Token in LineTokens:
        if Token.startswith("#"):
            break

        Tokens.append(Token)

Tokens.reverse()

class Expression:
    name = ""
    bodies = []

    def __init__(self, b, n = ""):
        self.name = n
        self.bodies = b

def generateBlocksFromTokens():
    Block = []

    while len(Tokens) > 0 and Tokens[-1] != "}":
        Token = Tokens.pop()

        # If expressions
        if Token == "if":
            # if { ... } else { ... }

            assert(Tokens.pop() == "{")
            IfBlock = (Token, Expression([generateBlocksFromTokens()]))
            assert(Tokens.pop() == "}")

            if len(Tokens) > 0 and Tokens[-1] == "else":
                Tokens.pop()    # Skip 'else' keyword

                assert(Tokens.pop() == "{")
                IfBlock[1].bodies.append(generateBlocksFromTokens())
                assert(Tokens.pop() == "}")
            
            Block.append(IfBlock)

        # While expressions
        elif Token == "while":
            # while { ... }

            assert(Tokens.pop() == "{")
            Block.append((Token, Expression([generateBlocksFromTokens()])))
            assert(Tokens.pop() == "}")
        
        # Functions
        elif Token == "fnn":
            # fnn <name> { ... }
            
            NAME = Tokens.pop()
            assert(Tokens.pop() == "{")
            Block.append((Token, Expression([generateBlocksFromTokens()], NAME)))
            assert(Tokens.pop() == "}")

        # Normal tokens
        else:
            Block.append((Token, None))
    
    return Block

Blocks = generateBlocksFromTokens()

### Interpreting
def printValue(val, end="\r\n"):
    if type(val) is bool:
        if val == True:
            print("Yes", end=end)
        elif val == False:
            print("No", end=end)
    else:
        print(val, end=end)

def assertIdenticalTypes(a, b):
    if not (type(a) is type(b)):
        reportError(f"Type '{type(a).__name__}' and '{type(b).__name__}' cannot be used together in an operation.")
        exit(1)

def assertType(a, t):
    if not (type(a) is t):
        reportError(f"Type '{type(a).__name__}' and '{t.__name__}' cannot be used together in an operation.")
        exit(1)

Stack = []

def assertMinStackSize(minSize):
    if len(Stack) < minSize:
        reportError(f"Expected at least {minSize} item(s) on stack to perform operation. Found {len(Stack)} instead.")
        exit(1)

Functions = []

def doesFunctionExist(name):
    for Func in Functions:
        if Func[0] == name:
            return True
    
    return False

def getFunctionWithName(name):
    for Func in Functions:
        if Func[0] == name:
            return Func
    
    return None

def interpretBlocks(Blocks):
    for Token, Expr in Blocks:
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


        ### Type-casting

        # toNum
        elif Token == "toNum":
            assertMinStackSize(1)
            VAL = Stack.pop()
            Stack.append(float(VAL))

        # toString
        elif Token == "toString":
            assertMinStackSize(1)
            VAL = Stack.pop()

            if type(VAL) is bool:
                if VAL == True:
                    Stack.append("Yes")
                elif VAL == False:
                    Stack.append("No")
            else:
                Stack.append(str(VAL))
        
        # toBool
        elif Token == "toBool":
            assertMinStackSize(1)
            VAL = Stack.pop()

            if type(VAL) is str:
                if VAL == "Yes":
                    Stack.append(True)
                elif VAL == "No":
                    Stack.append(False)
            else:
                Stack.append(bool(VAL))

            Stack.append(bool(VAL))

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
        
        # Duplicate
        elif Token == "dup":
            assertMinStackSize(1)
            VAL = Stack[-1]
            Stack.append(VAL)

        # Keyword 'printLine'
        elif Token == "printLine":
            assertMinStackSize(1)
            printValue(Stack.pop())

        # Keyword 'print'
        elif Token == "print":
            assertMinStackSize(1)
            printValue(Stack.pop(), end="")

        # Keyword 'readLine'
        elif Token == "readLine":
            LINE = input()
            Stack.append(LINE)

        # Keyword 'if'
        elif Token == "if":
            assertMinStackSize(1)
            COND = Stack.pop()
            assertType(COND, bool)

            if COND == True:
                interpretBlocks(Expr.bodies[0])
            elif len(Expr.bodies) == 2:
                interpretBlocks(Expr.bodies[1])

        # Keyword 'while'
        elif Token == "while":
            while True:
                assertMinStackSize(1)
                COND = Stack.pop()
                assertType(COND, bool)

                if not COND:
                    break
                
                interpretBlocks(Expr.bodies[0])
        
        # Keyword 'fnn'
        elif Token == "fnn":
            NAME = Expr.name
            BODY = Expr.bodies[0]
            Functions.append((NAME, BODY))

        # Function
        elif doesFunctionExist(Token):
            FUNC = getFunctionWithName(Token)
            interpretBlocks(FUNC[1])

        # Unknown token
        else:
            reportError(f"Unknown token '{Token}' found in '{Path}'.")
            exit(1)

interpretBlocks(Blocks)
