from doctest import (
    IGNORE_EXCEPTION_DETAIL,
    DocTest,
    DocTestParser,
    DocTestRunner,
)
from typing import Any, Callable


def run_doctests(
    target: type | Callable[..., Any],
    globs: dict[str, object] | None = None,
    out: Callable[[str], None] | None = None,
) -> None:
    """
    Runs doctests for a specific passed target.

    Args:
        target (type | Callable): some arbitrary Python callable or class.
            Please note when passing a class, only the class docstring is taken
            into account. There is no introspection against class methods.
        globs (dict): additional variables that must be declared for the
            doctest to run successfully. See :func:`parse_docstring_variables`
            to extract required dependencies from other docstrings.

    Raises:
        AssertionError: in case any doctest failed.
    """

    test = _get_doctest_from_object(target, globs)
    runner = DocTestRunner(optionflags=IGNORE_EXCEPTION_DETAIL)
    result = runner.run(test, out=out)
    if result.failed > 0:
        raise AssertionError()


def parse_docstring_variables(
    source: type | Callable[..., Any],
    globs: dict[str, object] | None = None,
) -> dict[str, object]:
    """
    Parses declared variables from a docstring.

    It might be the case that docstrings are structured in a manner as follows:

    .. code-block:: python
        class C:
            '''
            Arbitrary class. This docstring may also be in __init__ instead.

            >>> c = C()
            '''

            def x(self) -> int:
                '''
                Some other meaningless code.

                >>> c.x()  # intention for reader: 'c is initialized above'
                133742
                '''
                return 133742

    Anyway, it may not always be the desired behavior to always implicitly
    derive doctest dependencies magically so it's left to the user whether
    he wants to derive those using this function and pass them as further
    globs to :func:`run_doctests`.

    Args:
        source (type | Callable): some arbitrary Python callable or class.
            Please note when passing a class, only the class docstring is taken
            into account. There is no introspection against class methods.
        globs (dict): additional variables that must be declared for the
            doctest to run successfully. See :func:`parse_docstring_variables`
            to extract required dependencies from other docstrings.
    """
    if source.__doc__ is None:
        raise ValueError("source docstring mustn't be None")
    test = _get_doctest_from_object(source, globs)
    return _get_variables_assigned_within_doctest(test)


def _get_doctest_from_object(
    source: type | Callable[..., Any],
    globs: dict[str, object] | None = None,
) -> DocTest:
    parser = DocTestParser()
    if source.__doc__ is None:
        raise ValueError("cannot derive from unset docstring")
    return parser.get_doctest(
        source.__doc__,
        {
            source.__name__: source,
            **(globs or {}),
        },
        source.__name__,
        filename=None,
        lineno=None,
    )


def _get_variables_assigned_within_doctest(test: DocTest) -> dict[str, object]:
    assigned_locals: dict[str, object] = {}
    for example in test.examples:
        # NOTE this implementation is inherently unsafe. but a better one
        # might not be necessary as we should never see untrusted code here.
        # if more safety is required, consider using 'ast' for parsing into
        # 'ast.Assignment' and evaluating those, or investigate how 'doctest'
        # runs code.
        exec(example.source, test.globs, assigned_locals)
    return assigned_locals
