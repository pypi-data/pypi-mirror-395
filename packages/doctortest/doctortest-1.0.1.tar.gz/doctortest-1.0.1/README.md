# doctortest

`doctortest` is a simple python package with helpful functionality for writing
docstring-based tests.

## Less boilerplate for running doctests

Successful example:
```python
def some_function(value: int) -> int:
    """
    Doubles given `value` by 2.

    >>> some_function(0)
    0
    >>> some_function(1)
    2
    >>> some_function(314)
    628
    """
    return value * 2

class SomeModuleTests(unittest.TestCase):
    def test_some_function(self):
        run_doctests(some_function)
```

An example that fails with `AssertionError` in case at least one assertion
is failing:
```python
def some_function(value: int) -> int:
    """
    Doubles given `value` by 2.
    >>> some_function(0)
    -1
    """
    return value * 2

class SomeModuleTests(unittest.TestCase):
    with self.assertRaises(AssertionError):
        run_doctests(some_function)
```

## Exposing context from other docstrings

Docstrings might use variables defined in other scopes, as shown by the
following example:

```python
class Colossus:
    """
    Hello, I am Colossus, the doctor's dog.

    >>> colossus_the_first = Colossus(endurance=3, is_happy=True)
    """

    def __init__(self, endurance: int, is_happy: bool = False) -> None:
        """
        Colossus can be awakened with the following preconditions:

        >>> happy_colossus = Colossus(endurance=8, is_happy=True)
        >>> unhappy_colossus = Colossus(endurance=2)
        """
        self.endurance = endurance
        self.is_happy = is_happy

    def bark(self) -> str:
        """
        Barking as loud as the constructor parameters told me to.

        >>> colossus_the_first.bark()
        'WOOOF'
        >>> happy_colossus.bark()
        'WOOOOOOOOF'
        >>> unhappy_colossus.bark()
        'woof :('
        """
        noise = "W" + "O" * self.endurance + "F"
        if not self.is_happy:
            return noise.lower() + " :("
        return noise
```

Running the doctests as follows would **not** work because it would result
in `NameError: 'unhappy_colossus' is not defined`:

```python
class ColossusTests(TestCase):
    def test_bark(self):
        run_doctests(Colossus.bark, out=write_output)
```

But the following example using `parse_docstring_variables` **would** work:
```python
class ColossusTests(TestCase):
    def test_bark(self) -> None:
        run_doctests(
            Colossus.bark,
            globs={
                **parse_docstring_variables(Colossus),
                **parse_docstring_variables(
                    Colossus.__init__,
                    globs={"Colossus": Colossus},
                ),
            },
        )
```
