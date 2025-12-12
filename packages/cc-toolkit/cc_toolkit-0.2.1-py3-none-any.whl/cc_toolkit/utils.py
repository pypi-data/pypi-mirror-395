# cc_toolkit/utils.py - Utility functions for the cc_toolkit package
def greet(name: str) -> str:
    """
    Generate a greeting message.
    
    Args:
        name (str): The name to greet.
    
    Returns:
        str: A greeting message.
    """
    return f"Hello, {name}! Welcome to cc_toolkit."

def calculate(a: int, b: int, operation: str = "add") -> int:
    """
    Perform basic arithmetic operations.
    
    Args:
        a (int): First operand.
        b (int): Second operand.
        operation (str): Operation to perform. Options: "add", "subtract", "multiply", "divide".
    
    Returns:
        int: Result of the arithmetic operation.
    
    Raises:
        ValueError: If an invalid operation is provided.
        ZeroDivisionError: If dividing by zero.
    """
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a // b
    else:
        raise ValueError(f"Invalid operation: {operation}. Available operations: add, subtract, multiply, divide")
