"""
Helper class and functions to allow creating a calculated column expression more easily

All functions return a `CalculatedColumnExpression` instance, that tracks calculations performed on it to
generate the resulting expression.

Most functions in this class expect a `CalculatedColumnExpression` as input.
These can be generated using the `column` and `literal` function:

- `column()` expects the string name of a column in the dataset
- `literal()` expects either a float, or boolean value

The result of these functions can then be combined using the built-in python arithmetic operations.

>>> literal(1) + column("a") / column("b")

``{'+': [{'lit': [1.0]}, {'/': [{'ref': ['a']}, {'ref': ['b']}]}]}``

A variety of arithmetic functions are provided to allow creation of more complex mathematical expressions,
such as `sin`, `cos` or `abs`. These mirror the behaviour of the respective function in the `math` standard library.

"""
import math
import numbers
from typing import List, Union


def _validate_dict(d: dict):
    if "if" in d.keys():
        if len(d) != 3:
            raise ValueError("Missing key in if statement")
        if "then" not in d.keys():
            raise ValueError("Missing key in if statement")
        if "else" not in d.keys():
            raise ValueError("Missing key in if statement")
        for k in ["if", "then", "else"]:
            if not isinstance(d[k], dict):
                raise ValueError("Invalid argument to if statement")
            _validate_dict(d[k])
    else:
        if len(d) != 1:
            raise ValueError("Too many keys")
        k = next(iter(d.keys()))
        if not isinstance(k, str):
            raise TypeError("Invalid key type")
        if not isinstance(d[k], list):
            raise ValueError("Invalid value type")
        if k in ["lit", "ref", "const"]:
            if len(d[k]) != 1:
                raise ValueError("Invalid value format")
            if not isinstance(d[k][0], (bool, str, numbers.Real)):
                raise ValueError("Invalid value format")
        else:
            for i in d[k]:
                _validate_dict(i)


class CalculatedColumnExpression(dict):
    """
    Magic class for dealing with calculated column expressions

    Supports `+`, `-`, `*`, `/`, `**` arithmetic operators between instances of itself.

    Supports `>`, `>=`, `<`, `<=`, `==`, `!=` comparison operators between itself
    (returning another Calculated Column Expression. To perform actual comparison, call `to_dict()` first)

    Supports boolean combination using bitwise operators:

    - `~` equates to `not`
    - `|` equates to `or`
    - `&` equates to `and`
    """

    def __init__(self, *args, **kwargs):
        """
        Accepts the same arguments as dict().

        The passed arguments must represent a valid calculated column expression.
        We recommend you use the `literal()` and `column()` functions to construct valid
        expressions rather than instantiating this directly.
        """
        super().__init__(*args, **kwargs)
        try:
            _validate_dict(self)
        except (AttributeError, AssertionError) as e:
            raise ValueError(
                "Invalid argument to CalculatedColumnExpression"
            ) from e

    def __add__(self, other) -> "CalculatedColumnExpression":
        if isinstance(other, float):
            other = CalculatedColumnExpression.lit(other)
        elif isinstance(other, int):
            other = CalculatedColumnExpression.lit(float(other))
        elif isinstance(other, str):
            other = CalculatedColumnExpression.col(other)
        return CalculatedColumnExpression({"+": [self, other]})

    def __sub__(self, other) -> "CalculatedColumnExpression":
        if isinstance(other, float):
            other = CalculatedColumnExpression.lit(other)
        elif isinstance(other, int):
            other = CalculatedColumnExpression.lit(float(other))
        elif isinstance(other, str):
            other = CalculatedColumnExpression.col(other)
        return CalculatedColumnExpression({"-": [self, other]})

    def __mul__(self, other) -> "CalculatedColumnExpression":
        if isinstance(other, float):
            other = CalculatedColumnExpression.lit(other)
        elif isinstance(other, int):
            other = CalculatedColumnExpression.lit(float(other))
        elif isinstance(other, str):
            other = CalculatedColumnExpression.col(other)
        return CalculatedColumnExpression({"*": [self, other]})

    def __pow__(self, other) -> "CalculatedColumnExpression":
        if isinstance(other, float):
            other = CalculatedColumnExpression.lit(other)
        elif isinstance(other, int):
            other = CalculatedColumnExpression.lit(float(other))
        elif isinstance(other, str):
            other = CalculatedColumnExpression.col(other)
        return CalculatedColumnExpression({"^": [self, other]})

    def __truediv__(self, other) -> "CalculatedColumnExpression":
        if isinstance(other, float):
            other = CalculatedColumnExpression.lit(other)
        elif isinstance(other, int):
            other = CalculatedColumnExpression.lit(float(other))
        elif isinstance(other, str):
            other = CalculatedColumnExpression.col(other)
        return CalculatedColumnExpression({"/": [self, other]})

    def __radd__(self, other) -> "CalculatedColumnExpression":
        if isinstance(other, float):
            other = CalculatedColumnExpression.lit(other)
        elif isinstance(other, int):
            other = CalculatedColumnExpression.lit(float(other))
        elif isinstance(other, str):
            other = CalculatedColumnExpression.col(other)
        return CalculatedColumnExpression({"+": [other, self]})

    def __rsub__(self, other) -> "CalculatedColumnExpression":
        if isinstance(other, float):
            other = CalculatedColumnExpression.lit(other)
        elif isinstance(other, int):
            other = CalculatedColumnExpression.lit(float(other))
        elif isinstance(other, str):
            other = CalculatedColumnExpression.col(other)
        return CalculatedColumnExpression({"-": [other, self]})

    def __rmul__(self, other) -> "CalculatedColumnExpression":
        if isinstance(other, float):
            other = CalculatedColumnExpression.lit(other)
        elif isinstance(other, int):
            other = CalculatedColumnExpression.lit(float(other))
        elif isinstance(other, str):
            other = CalculatedColumnExpression.col(other)
        return CalculatedColumnExpression({"*": [other, self]})

    def __rpow__(self, other) -> "CalculatedColumnExpression":
        if isinstance(other, float):
            other = CalculatedColumnExpression.lit(other)
        elif isinstance(other, int):
            other = CalculatedColumnExpression.lit(float(other))
        elif isinstance(other, str):
            other = CalculatedColumnExpression.col(other)
        return CalculatedColumnExpression({"^": [other, self]})

    def __rtruediv__(self, other) -> "CalculatedColumnExpression":
        if isinstance(other, float):
            other = CalculatedColumnExpression.lit(other)
        elif isinstance(other, int):
            other = CalculatedColumnExpression.lit(float(other))
        elif isinstance(other, str):
            other = CalculatedColumnExpression.col(other)
        return CalculatedColumnExpression({"/": [other, self]})

    def __abs__(self) -> "CalculatedColumnExpression":
        return CalculatedColumnExpression({"abs": [self]})

    def __gt__(self, other) -> "CalculatedColumnExpression":
        if isinstance(other, float):
            other = CalculatedColumnExpression.lit(other)
        elif isinstance(other, int):
            other = CalculatedColumnExpression.lit(float(other))
        elif isinstance(other, str):
            other = CalculatedColumnExpression.col(other)
        return CalculatedColumnExpression({">": [self, other]})

    def __ge__(self, other) -> "CalculatedColumnExpression":
        if isinstance(other, float):
            other = CalculatedColumnExpression.lit(other)
        elif isinstance(other, int):
            other = CalculatedColumnExpression.lit(float(other))
        elif isinstance(other, str):
            other = CalculatedColumnExpression.col(other)
        return CalculatedColumnExpression({">=": [self, other]})

    def __lt__(self, other) -> "CalculatedColumnExpression":
        if isinstance(other, float):
            other = CalculatedColumnExpression.lit(other)
        elif isinstance(other, int):
            other = CalculatedColumnExpression.lit(float(other))
        elif isinstance(other, str):
            other = CalculatedColumnExpression.col(other)
        return CalculatedColumnExpression({"<": [self, other]})

    def __le__(self, other) -> "CalculatedColumnExpression":
        if isinstance(other, float):
            other = CalculatedColumnExpression.lit(other)
        elif isinstance(other, int):
            other = CalculatedColumnExpression.lit(float(other))
        elif isinstance(other, str):
            other = CalculatedColumnExpression.col(other)
        return CalculatedColumnExpression({"<=": [self, other]})

    def __eq__(self, other) -> "CalculatedColumnExpression":
        if isinstance(other, float):
            other = CalculatedColumnExpression.lit(other)
        elif isinstance(other, int):
            other = CalculatedColumnExpression.lit(float(other))
        elif isinstance(other, str):
            other = CalculatedColumnExpression.col(other)
        return CalculatedColumnExpression({"=": [self, other]})

    def __ne__(self, other) -> "CalculatedColumnExpression":
        if isinstance(other, float):
            other = CalculatedColumnExpression.lit(other)
        elif isinstance(other, int):
            other = CalculatedColumnExpression.lit(float(other))
        elif isinstance(other, str):
            other = CalculatedColumnExpression.col(other)
        return CalculatedColumnExpression({"!=": [self, other]})

    def __and__(self, other) -> "CalculatedColumnExpression":
        if isinstance(other, bool):
            other = _CCE.lit(other)
        return CalculatedColumnExpression({"and": [self, other]})

    def __rand__(self, other) -> "CalculatedColumnExpression":
        if isinstance(other, bool):
            other = _CCE.lit(other)
        return CalculatedColumnExpression({"and": [other, self]})

    def __or__(self, other) -> "CalculatedColumnExpression":
        if isinstance(other, bool):
            other = _CCE.lit(other)
        return CalculatedColumnExpression({"or": [self, other]})

    def __ror__(self, other) -> "CalculatedColumnExpression":
        if isinstance(other, bool):
            other = _CCE.lit(other)
        return CalculatedColumnExpression({"or": [other, self]})

    def __invert__(self):
        return CalculatedColumnExpression({"not": [self]})

    def apply(self, func: str) -> "CalculatedColumnExpression":
        return CalculatedColumnExpression({str(func): [self]})

    @staticmethod
    def if_(
        cond: "CalculatedColumnExpression",
        true_: "CalculatedColumnExpression",
        false_: "CalculatedColumnExpression",
    ) -> "CalculatedColumnExpression":
        if (
            not isinstance(cond, CalculatedColumnExpression)
            or not isinstance(true_, CalculatedColumnExpression)
            or not isinstance(false_, CalculatedColumnExpression)
        ):
            raise TypeError(
                "All arguments to if_ must be CalculatedColumnExpressions"
            )
        return CalculatedColumnExpression(
            {"if": cond, "then": true_, "else": false_}
        )

    @staticmethod
    def col(other) -> "CalculatedColumnExpression":
        if isinstance(other, dict):
            if "ref" not in other:
                raise ValueError("Invalid argument to col")
            return CalculatedColumnExpression(other)
        elif isinstance(other, str):
            return CalculatedColumnExpression({"ref": [other]})
        else:
            return CalculatedColumnExpression({"ref": [str(other)]})

    @staticmethod
    def lit(other) -> "CalculatedColumnExpression":
        if isinstance(other, dict):
            if "lit" not in other:
                raise ValueError("Invalid argument to lit")
            return CalculatedColumnExpression(other)
        elif isinstance(other, float):
            return CalculatedColumnExpression({"lit": [other]})
        elif isinstance(other, bool):
            return CalculatedColumnExpression({"lit": [other]})
        else:
            return CalculatedColumnExpression({"lit": [float(other)]})

    @staticmethod
    def const(other) -> "CalculatedColumnExpression":
        if isinstance(other, dict):
            if "const" not in other:
                raise ValueError("Invalid argument to const")
            return CalculatedColumnExpression(other)
        elif isinstance(other, str):
            if other not in {"nan", "pi", "e"}:
                raise ValueError("Invalid argument to const")
            return CalculatedColumnExpression({"const": [other]})
        else:
            raise ValueError("Invalid argument to const")

    def __setitem__(self, key, value):
        raise TypeError("Updating CalculatedColumnExpressions not supported")

    def __delitem__(self, key):
        raise TypeError("Updating CalculatedColumnExpressions not supported")

    def update(self, __m, **kwargs):
        raise TypeError("Updating CalculatedColumnExpressions not supported")

    def setdefault(self, *args, **kwargs):
        raise TypeError("Updating CalculatedColumnExpressions not supported")

    def pop(self, __key):
        raise TypeError("Updating CalculatedColumnExpressions not supported")

    def popitem(self):
        raise TypeError("Updating CalculatedColumnExpressions not supported")

    def get_operator(self):
        if len(self) == 3:
            assert "if" in self.keys()
            return "if"
        else:
            assert len(self) == 1
            return next(iter(self.keys()))

    def get_arguments(self):
        if self.get_operator() == "if":
            return [self["if"], self["then"], self["else"]]
        else:
            return self[self.get_operator()]

    def to_dict(self) -> dict:
        if self.get_operator() == "if":
            return {
                "if": self["if"].to_dict(),
                "then": self["then"].to_dict(),
                "else": self["else"].to_dict(),
            }
        else:
            op = self.get_operator()
            return {
                op: [
                    x.to_dict()
                    if isinstance(x, CalculatedColumnExpression)
                    else x
                    for x in self.get_arguments()
                ]
            }


_CCE = CalculatedColumnExpression


def column(col: str) -> _CCE:
    return _CCE.col(col)


e = _CCE.const("e")

pi = _CCE.const("pi")

nan = _CCE.const("nan")


def literal(val: Union[int, float, bool]) -> _CCE:
    if isinstance(val, float):
        if val == math.pi:
            return _CCE.const("pi")
        elif val == math.e:
            return _CCE.const("e")
        elif math.isnan(val):
            return _CCE.const("nan")
    return _CCE.lit(val)


# Arithmetic expressions
def ln(element: _CCE) -> _CCE:
    return element.apply("ln")


def sin(element: _CCE) -> _CCE:
    return element.apply("sin")


def asin(element: _CCE) -> _CCE:
    return element.apply("asin")


def cos(element: _CCE) -> _CCE:
    return element.apply("cos")


def acos(element: _CCE) -> _CCE:
    return element.apply("acos")


def tan(element: _CCE) -> _CCE:
    return element.apply("tan")


def atan(element: _CCE) -> _CCE:
    return element.apply("atan")


def abs_(element: _CCE) -> _CCE:
    return element.apply("abs")


def sqrt(element: _CCE) -> _CCE:
    return element.apply("sqrt")


def sinh(element: _CCE) -> _CCE:
    return element.apply("sinh")


def asinh(element: _CCE) -> _CCE:
    return element.apply("asinh")


def cosh(element: _CCE) -> _CCE:
    return element.apply("cosh")


def acosh(element: _CCE) -> _CCE:
    return element.apply("acosh")


def tanh(element: _CCE) -> _CCE:
    return element.apply("tanh")


def atanh(element: _CCE) -> _CCE:
    return element.apply("atanh")


# Aggregate functions
def sum_(elements: List[_CCE]) -> _CCE:
    if len(elements) == 0:
        raise ValueError("Must have at least one argument")
    if not all(isinstance(x, CalculatedColumnExpression) for x in elements):
        raise TypeError(
            "All elements must be CalculatedColumnExpression instances"
        )
    if len(elements) == 1:
        return elements[0]
    return _CCE({"sum": elements})


def product(elements: List[_CCE]) -> _CCE:
    if len(elements) == 0:
        raise ValueError("Must have at least one argument")
    if not all(isinstance(x, CalculatedColumnExpression) for x in elements):
        raise TypeError(
            "All elements must be CalculatedColumnExpression instances"
        )
    if len(elements) == 1:
        return elements[0]
    return _CCE({"product": elements})


def min_(elements: List[_CCE]) -> _CCE:
    if len(elements) == 0:
        raise ValueError("Must have at least one argument")
    if not all(isinstance(x, CalculatedColumnExpression) for x in elements):
        raise TypeError(
            "All elements must be CalculatedColumnExpression instances"
        )
    if len(elements) == 1:
        return elements[0]
    return _CCE({"min": elements})


def max_(elements: List[_CCE]) -> _CCE:
    if len(elements) == 0:
        raise ValueError("Must have at least one argument")
    if not all(isinstance(x, CalculatedColumnExpression) for x in elements):
        raise TypeError(
            "All elements must be CalculatedColumnExpression instances"
        )
    if len(elements) == 1:
        return elements[0]
    return _CCE({"max": elements})


def mean(elements: List[_CCE]) -> _CCE:
    if len(elements) == 0:
        raise ValueError("Must have at least one argument")
    if not all(isinstance(x, CalculatedColumnExpression) for x in elements):
        raise TypeError(
            "All elements must be CalculatedColumnExpression instances"
        )
    if len(elements) == 1:
        return elements[0]
    return _CCE({"avg": elements})


def avg(elements: List[_CCE]) -> _CCE:
    if len(elements) == 0:
        raise ValueError("Must have at least one argument")
    if not all(isinstance(x, CalculatedColumnExpression) for x in elements):
        raise TypeError(
            "All elements must be CalculatedColumnExpression instances"
        )
    if len(elements) == 1:
        return elements[0]
    return _CCE({"avg": elements})


# Conditional expression
def if_(test: _CCE, true: _CCE, false: _CCE) -> _CCE:
    return _CCE.if_(test, true, false)
