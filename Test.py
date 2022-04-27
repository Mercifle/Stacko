#!/usr/bin/env python3
import subprocess
import glob

ReturnCode = 0

def passTest(TestName):
    print(f"\033[32;1m[PASS]\033[0m {TestName}")

def failTest(TestName):
    print(f"\033[31;1m[FAIL]\033[0m {TestName}")
    global ReturnCode
    ReturnCode += 1

Tests = glob.glob("Tests/*.stko")
Tests += glob.glob("Tests/*.stacko")

for Test in Tests:
    proc = subprocess.run([ "./Stacko.py", Test ], capture_output=True)
    
    if proc.returncode == 0:
        passTest(Test)
    else:
        failTest(Test)