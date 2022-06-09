#!/usr/bin/env python3
import sys
import re

### Error reporting
def reportError(msg, emoji="😭"):
    print(f"\33[31mError\33[0m: \33[32m{msg}\33[0m {emoji}", file=sys.stderr)

ARGS = sys.argv

if len(ARGS) != 2:
    reportError("No file given")
    exit(1)

Path = ARGS[1]

Imports = []

def collectImports(FilePath):
    # Make sure file uses the '.stko' or '.stacko' extension
    if not (FilePath.endswith(".stko") or FilePath.endswith(".stacko")):
        reportError("Extension was not '.stko' or '.stacko'")
        exit(1)

    try:
        File = open(FilePath, "r")
        Words = File.read().split()
        File.close()
    except:
        reportError(f"Failed to open '{FilePath}'. No such file exists", "😐🔍")
        exit(1)
    
    for I, Word in enumerate(Words):
        # import <file path>
        if Word == "file":
            ImportPath = Words[I + 1]

            if ImportPath in Imports:
                continue

            Imports.append(ImportPath)
            collectImports(ImportPath)

def collectTokensFromFile(FilePath):
    # Make sure file uses the '.stko' or '.stacko' extension
    if not (FilePath.endswith(".stko") or FilePath.endswith(".stacko")):
        reportError("Extension was not '.stko' or '.stacko'")
        exit(1)

    try:
        File = open(FilePath, "r")
        ContentLines = File.readlines()
        File.close()
    except:
        reportError(f"Failed to open '{FilePath}'. No such file exists", "😐🔍")
        exit(1)

    Tokens = []

    # Collect tokens, discarding tokens after the '#' symbol (comments)
    for Line in ContentLines:
        LineTokens = re.findall("(?:\".*?\"|\S)+", Line)

        if len(LineTokens) > 0 and LineTokens[0] == "file":
            continue

        for Token in LineTokens:
            if Token.startswith("#"):
                break

            Tokens.append(Token)
    
    return Tokens

### Collect imports
collectImports(Path)
Imports.reverse()

Tokens = []

for ImportPath in Imports:
    Tokens += collectTokensFromFile(ImportPath)

Tokens += collectTokensFromFile(Path)
Tokens.reverse()

class Expression:
    name = ""
    bodies = []

    def __init__(self, b, n = ""):
        self.name = n
        self.bodies = b

def expectToken(Val):
    if len(Tokens) == 0:
        reportError(f"Expected '{Val}', found nothing instead", "😐🔍")
        exit(1)
    
    TOKEN = Tokens.pop()
    if TOKEN != Val:
        reportError(f"Expected '{Val}', found {TOKEN} instead", "😐🔍")
        exit(1)

def generateBlocksFromTokens():
    Block = []

    while len(Tokens) > 0 and Tokens[-1] != "}":
        Token = Tokens.pop()

        # If expressions
        if Token == "if":
            # if { ... } else { ... }

            expectToken("{")
            IfBlock = (Token, Expression([generateBlocksFromTokens()]))
            expectToken("}")

            if len(Tokens) > 0 and Tokens[-1] == "else":
                Tokens.pop()    # Skip 'else' keyword

                expectToken("{")
                IfBlock[1].bodies.append(generateBlocksFromTokens())
                expectToken("}")
            
            Block.append(IfBlock)

        # While expressions
        elif Token == "while":
            # while { ... }

            expectToken("{")
            Block.append((Token, Expression([generateBlocksFromTokens()])))
            expectToken("}")
        
        # Functions
        elif Token == "fnn":
            # fnn <name> { ... }
            
            NAME = Tokens.pop()
            expectToken("{")
            Block.append((Token, Expression([generateBlocksFromTokens()], NAME)))
            expectToken("}")

        # Constants
        elif Token == "const":
            # const <name>

            NAME = Tokens.pop()
            Block.append((Token, Expression(None, NAME)))

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

Constants = []

def doesConstantExist(name):
    for Const in Constants:
        if Const[0] == name:
            return True
    
    return False

def getConstantWithName(name):
    for Const in Constants:
        if Const[0] == name:
            return Const
    
    return None

def doesNameExist(name):
    if getFunctionWithName(name) != None:
        return True
    if getConstantWithName(name) != None:
        return True
    
    return False

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

        # Modulo
        elif Token == "%":
            assertMinStackSize(2)
            A = Stack.pop()
            B = Stack.pop()
            assertIdenticalTypes(A, B)

            RESULT = B % A
            Stack.append(RESULT)

        # Equality
        elif Token == "=":
            assertMinStackSize(2)
            A = Stack.pop()
            B = Stack.pop()
            assertIdenticalTypes(A, B)

            RESULT = (B == A)
            Stack.append(RESULT)

        # Greater than
        elif Token == ">":
            assertMinStackSize(2)
            A = Stack.pop()
            assertType(A, float)
            B = Stack.pop()
            assertType(B, float)

            RESULT = B > A
            Stack.append(RESULT)

        # Less than
        elif Token == "<":
            assertMinStackSize(2)
            A = Stack.pop()
            assertType(A, float)
            B = Stack.pop()
            assertType(B, float)

            RESULT = B < A
            Stack.append(RESULT)

        # Greater than or equal to
        elif Token == ">=":
            assertMinStackSize(2)
            A = Stack.pop()
            assertType(A, float)
            B = Stack.pop()
            assertType(B, float)

            RESULT = B >= A
            Stack.append(RESULT)

        # Less than or equal to
        elif Token == "<=":
            assertMinStackSize(2)
            A = Stack.pop()
            assertType(A, float)
            B = Stack.pop()
            assertType(B, float)

            RESULT = B <= A
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

        # Pop
        elif Token == "pop":
            assertMinStackSize(1)
            Stack.pop()

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
        
        # Keyowrd 'exit'
        elif Token == "exit":
            assertMinStackSize(1)
            RETURN_CODE = Stack.pop()
            assertType(RETURN_CODE, float)
            exit(int(RETURN_CODE))

        ### Assertions
        
        # Keyword 'assert'
        elif Token == "assert":
            assertMinStackSize(1)
            VAL = Stack.pop()
            assertType(VAL, bool)
            
            if not VAL:
                reportError(f"Assertion failed.")
                exit(2)
        
        # Keyword 'assertEqual'
        elif Token == "assertEqual":
            assertMinStackSize(2)
            A = Stack.pop()
            B = Stack.pop()
            assertIdenticalTypes(A, B)
            
            if A != B:
                reportError(f"Assertion failed. Values were not equal.")
                exit(2)

        # Keyword 'assertNotEqual'
        elif Token == "assertNotEqual":
            assertMinStackSize(2)
            A = Stack.pop()
            B = Stack.pop()
            assertIdenticalTypes(A, B)
            
            if A == B:
                reportError(f"Assertion failed. Values were equal.")
                exit(2)

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
            if doesNameExist(NAME):
                reportError(f"Name '{NAME}' already exists elsewhere.")
                exit(1)
            
            Functions.append((NAME, BODY))

        # Keyword 'const'
        elif Token == "const":
            assertMinStackSize(1)
            NAME = Expr.name

            if doesNameExist(NAME):
                reportError(f"Name '{NAME}' already exists elsewhere.")
                exit(1)
            
            VAL = Stack.pop()
            Constants.append((NAME, VAL))

        # Function
        elif doesFunctionExist(Token):
            FUNC = getFunctionWithName(Token)
            interpretBlocks(FUNC[1])
        
        # Constant
        elif doesConstantExist(Token):
            CONST = getConstantWithName(Token)
            Stack.append(CONST[1])

        # Unknown token
        else:
            reportError(f"Unknown token '{Token}' found in '{Path}'.")
            exit(1)

interpretBlocks(Blocks)
