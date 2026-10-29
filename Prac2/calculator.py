def add(a,b):
    return a + b

def subtract(a,b):
    return a - b

def multiply(a,b):
    return a * b

def divide(a,b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Run steps for Prac2:
# 1. Open terminal in this folder.
# 2. Run: python -m pytest -q
# 3. Optional: import calculator in a Python shell and test functions manually.
