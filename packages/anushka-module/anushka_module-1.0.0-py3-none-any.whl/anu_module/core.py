# Module is collection of functions and classes
# Module is a file containing Python code
# Module is used to organize code into manageable sections 
# Module can be imported and reused in other Python files
# Module can define variables, functions, and classes
# Example of a simple module
cretor = "Anushka"
orgnaization = "OpenAI"

def greet(name):
    return f"Hello, {name}!"

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b    

def divide(a, b):
    if b != 0:
        return a / b
    else:
        return "Cannot divide by zero"
def table_of(number):
    return [number * i for i in range(1, 11)]
    
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

def is_even(n):
    return n % 2 == 0

def pallindrome(s):
    return s == s[::-1]

def prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
