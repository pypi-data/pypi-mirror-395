from unittest import TestCase

from doctortest import parse_docstring_variables, run_doctests


class RunDoctestsTests(TestCase):
    def test_success(self) -> None:
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

        run_doctests(some_function)

    def test_fail(self) -> None:
        def some_function(value: int) -> int:
            """
            Doubles given `value` by 2.

            >>> some_function(0)
            -1
            """
            return value * 2

        with self.assertRaises(AssertionError):
            run_doctests(some_function, out=lambda _: None)


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


class ParseDocstringVariablesTests(TestCase):
    def test_run_doctests_with_parsed_dependencies(self) -> None:
        """
        Demonstrates how dependencies from docstrings amongst each other
        are intended to be resolved
        """

        output = ""

        def write_output(value: str) -> None:
            nonlocal output
            output += value

        # The doctests won't run without giving them the variables other
        # doctests define.
        with self.assertRaises(AssertionError):
            run_doctests(Colossus.bark, out=write_output)
        self.assertIn(
            "NameError: name 'unhappy_colossus' is not defined", output
        )

        # With passing them using parse_docstring_variables() they should pass:
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
