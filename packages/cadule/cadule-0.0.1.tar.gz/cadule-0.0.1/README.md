# Cadule

*Cadule* (short for Ca\[llableMo\]dule) is a Python library that transforms regular modules into callable objects. By using the decorators provided by cadule, you can make entire modules callable just like functions.

## Usage 

### Example File: `hello.py`

```python
import cadule

@cadule
def __call__():
    print("Hello World!")
```

### Python REPL Interaction

```python
>>> import hello
>>> hello()
Hello World!
>>> # Now the entire hello module has become a callable object
>>> callable(hello)
True
>>> # You can still access other attributes in the module (if any exist)
```

As shown above, by simply applying the decorator, the entire `hello` module becomes a callable object, and calling it executes the decorated `__call__` function.
