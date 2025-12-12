# cc-toolkit

A Python toolkit for common tasks.

## Installation

You can install cc-toolkit using pip:

```bash
pip install cc-toolkit
```

## Usage

### Greeting Function

```python
from cc_toolkit import greet

# Generate a greeting message
message = greet("World")
print(message)  # Output: Hello, World! Welcome to cc_toolkit.
```

### Calculator Function

```python
from cc_toolkit import calculate

# Addition
result = calculate(5, 3, "add")
print(f"5 + 3 = {result}")  # Output: 5 + 3 = 8

# Subtraction
result = calculate(5, 3, "subtract")
print(f"5 - 3 = {result}")  # Output: 5 - 3 = 2

# Multiplication
result = calculate(5, 3, "multiply")
print(f"5 * 3 = {result}")  # Output: 5 * 3 = 15

# Division
result = calculate(6, 3, "divide")
print(f"6 / 3 = {result}")  # Output: 6 / 3 = 2
```

## Features

- Simple greeting function
- Basic arithmetic operations
- Easy to extend with new functionality

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
