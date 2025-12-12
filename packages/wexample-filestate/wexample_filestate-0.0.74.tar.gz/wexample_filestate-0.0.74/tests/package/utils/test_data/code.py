from __future__ import annotations


def hello_function() -> str:
    """A simple hello function."""
    print("Hello, world!")
    return "hello"


class HelloClass:
    def __init__(self) -> None:
        self.greeting = "hello"

    def say_hello(self):
        return f"{self.greeting} from class"


# Test comment with hello
hello_var = "hello world"
another_hello = hello_function()
