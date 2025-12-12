import numbers

import numpy as np
import pytest
from alchemite_apiclient import calculated_columns as cc

CCE = cc.CalculatedColumnExpression


def assert_binary_op(key, res: CCE, val1, val2):
    assert len(res) == 1
    assert key in res
    assert res.get_operator() == key
    assert len(res[key]) == 2

    if isinstance(val1, str):
        val1 = cc.column(val1)
    elif isinstance(val1, (numbers.Real, bool)):
        val1 = cc.literal(val1)

    if isinstance(val2, str):
        val2 = cc.column(val2)
    elif isinstance(val2, (numbers.Real, bool)):
        val2 = cc.literal(val2)
    res_dict = res.to_dict()
    val1_dict = val1.to_dict()
    val2_dict = val2.to_dict()

    assert res_dict[key] == [val1_dict, val2_dict]
    assert [x.to_dict() for x in res.get_arguments()] == [val1_dict, val2_dict]


def assert_if_op(res: CCE, test, val1, val2):
    assert len(res) == 3
    assert "if" in res
    assert "then" in res
    assert "else" in res
    assert res.get_operator() == "if"

    assert res["if"].to_dict() == test.to_dict()
    assert res["then"].to_dict() == val1.to_dict()
    assert res["else"].to_dict() == val2.to_dict()
    assert [x.to_dict() for x in res.get_arguments()] == [
        test.to_dict(),
        val1.to_dict(),
        val2.to_dict(),
    ]
    assert res.to_dict() == {
        "if": test.to_dict(),
        "then": val1.to_dict(),
        "else": val2.to_dict(),
    }


def assert_unary_op(key, res, val):
    assert len(res) == 1
    assert key in res
    assert len(res[key]) == 1
    assert [x.to_dict() for x in res[key]] == [val.to_dict()]


@pytest.mark.parametrize(
    "input_dict,error",
    [
        pytest.param({"ln": [{"lit": [2.0]}]}, None, id="valid_float"),
        pytest.param(
            {"ln": [{"lit": [np.float32(2.0)]}]}, None, id="valid_exotic"
        ),
        pytest.param({"ln": [2.0]}, ValueError, id="missing_lit"),
        pytest.param({2: [{"lit": [2.0]}]}, TypeError, id="invalid_key_type"),
        pytest.param({"ref": [{"ref": [2.0]}]}, ValueError, id="nested_refs"),
        pytest.param(
            {"ln": [{"lit": [2.0, 3.0]}]}, ValueError, id="multi_float"
        ),
        pytest.param(
            {"ln": [{"lit": [2.0]}], "sum": [{"lit": [2.0]}]},
            ValueError,
            id="multiple_keys",
        ),
        pytest.param(
            {
                "if": {"lit": [True]},
                "then": {"lit": [2.0]},
                "else": {"ref": ["a"]},
            },
            None,
            id="valid_if",
        ),
        pytest.param(
            {"if": {"lit": [True]}, "then": {"lit": [2.0]}},
            ValueError,
            id="partial_if",
        ),
        pytest.param({"then": {"lit": [2.0]}}, ValueError, id="just_then"),
        pytest.param(
            {
                "if": {"lit": [True]},
                "than": {"lit": [2.0]},
                "else": {"ref": ["a"]},
            },
            ValueError,
            id="if_typo",
        ),
        pytest.param(
            {
                "if": {"lit": [True]},
                "then": {"lit": [2.0]},
                "alse": {"ref": ["a"]},
            },
            ValueError,
            id="if_typo2",
        ),
        pytest.param(
            {
                "if": [{"lit": [True]}],
                "then": [{"lit": [2.0]}],
                "else": [{"ref": ["a"]}],
            },
            ValueError,
            id="listed_if",
        ),
    ],
)
def test_validation(input_dict, error):
    if error is not None:
        with pytest.raises(error):
            CCE(input_dict)
    else:
        CCE(input_dict)


@pytest.mark.parametrize(
    "val1,val2",
    [
        pytest.param(cc.literal(2.0), cc.column("a"), id="both_cce"),
        pytest.param(cc.column("a"), 2.0, id="cce_float"),
        pytest.param(cc.column("a"), 2, id="cce_int"),
        pytest.param(cc.column("a"), "b", id="cce_str"),
        pytest.param(2.0, cc.column("a"), id="float_cce"),
        pytest.param(2, cc.column("a"), id="int_cce"),
        pytest.param("b", cc.column("a"), id="str_cce"),
    ],
)
def test_arithmetic_ops(val1, val2):
    plus = val1 + val2
    assert_binary_op("+", plus, val1, val2)

    minus = val1 - val2
    assert_binary_op("-", minus, val1, val2)

    times = val1 * val2
    assert_binary_op("*", times, val1, val2)

    div = val1 / val2
    assert_binary_op("/", div, val1, val2)

    exp = val1**val2
    assert_binary_op("^", exp, val1, val2)


def test_abs():
    val = cc.literal(2.0)
    ab = abs(val)
    assert_unary_op("abs", ab, val)


@pytest.mark.parametrize(
    "val1,val2,flipped",
    [
        pytest.param(cc.literal(2.0), cc.column("a"), False, id="both_cce"),
        pytest.param(cc.column("a"), 2.0, False, id="cce_float"),
        pytest.param(cc.column("a"), 2, False, id="cce_int"),
        pytest.param(cc.column("a"), "b", False, id="cce_str"),
        pytest.param(2.0, cc.column("a"), True, id="float_cce"),
        pytest.param(2, cc.column("a"), True, id="int_cce"),
        pytest.param("b", cc.column("a"), True, id="str_cce"),
    ],
)
def test_comparison_ops(val1, val2, flipped):
    lt = val1 < val2
    if flipped:
        assert_binary_op(">", lt, val2, val1)
    else:
        assert_binary_op("<", lt, val1, val2)

    lte = val1 <= val2
    if flipped:
        assert_binary_op(">=", lte, val2, val1)
    else:
        assert_binary_op("<=", lte, val1, val2)

    gt = val1 > val2

    if flipped:
        assert_binary_op("<", gt, val2, val1)
    else:
        assert_binary_op(">", gt, val1, val2)

    gte = val1 >= val2
    if flipped:
        assert_binary_op("<=", gte, val2, val1)
    else:
        assert_binary_op(">=", gte, val1, val2)

    eq = val1 == val2
    if flipped:
        assert_binary_op("=", eq, val2, val1)
    else:
        assert_binary_op("=", eq, val1, val2)

    ne = val1 != val2
    if flipped:
        assert_binary_op("!=", ne, val2, val1)
    else:
        assert_binary_op("!=", ne, val1, val2)


@pytest.mark.parametrize(
    "val1,val2",
    [
        pytest.param(cc.literal(True), cc.literal(False), id="both_cce"),
        pytest.param(cc.literal(True), True, id="cce_bool"),
        pytest.param(True, cc.literal(True), id="bool_cce"),
    ],
)
def test_boolean_ops(val1, val2):
    or_ = val1 | val2
    assert_binary_op("or", or_, val1, val2)

    and_ = val1 & val2
    assert_binary_op("and", and_, val1, val2)


def test_boolean_not():
    val = cc.literal(True)
    ab = ~val
    assert_unary_op("not", ab, val)


@pytest.mark.parametrize(
    "func,name",
    [
        pytest.param(cc.ln, "ln", id="ln"),
        pytest.param(cc.sin, "sin", id="sin"),
        pytest.param(cc.asin, "asin", id="asin"),
        pytest.param(cc.cos, "cos", id="cos"),
        pytest.param(cc.acos, "acos", id="acos"),
        pytest.param(cc.tan, "tan", id="tan"),
        pytest.param(cc.atan, "atan", id="atan"),
        pytest.param(cc.abs_, "abs", id="abs"),
        pytest.param(cc.sqrt, "sqrt", id="sqrt"),
        pytest.param(cc.sinh, "sinh", id="sinh"),
        pytest.param(cc.asinh, "asinh", id="asinh"),
        pytest.param(cc.cosh, "cosh", id="cosh"),
        pytest.param(cc.acosh, "acosh", id="acosh"),
        pytest.param(cc.tanh, "tanh", id="tanh"),
        pytest.param(cc.atanh, "atanh", id="atanh"),
    ],
)
def test_single_func(func, name):
    val = cc.column("a")
    assert_unary_op(name, func(val), val)


@pytest.mark.parametrize(
    "func,name",
    [
        pytest.param(cc.sum_, "sum", id="sum"),
        pytest.param(cc.product, "product", id="product"),
        pytest.param(cc.min_, "min", id="min"),
        pytest.param(cc.max_, "max", id="max"),
        pytest.param(cc.avg, "avg", id="avg"),
        pytest.param(cc.mean, "avg", id="avg"),
    ],
)
@pytest.mark.parametrize(
    "args,error",
    [
        pytest.param([cc.column("a"), cc.column("b")], None, id="valid"),
        pytest.param([cc.column("a")], None, id="single"),
        pytest.param([], ValueError, id="empty"),
        pytest.param(
            [cc.column("a"), {"lit": [2.0]}], TypeError, id="raw_dict"
        ),
        pytest.param([cc.column("a"), 2.0], TypeError, id="raw_float"),
    ],
)
def test_list_funcs(func, name, args, error):
    if error is not None:
        with pytest.raises(error):
            func(args)
    else:
        if len(args) == 1:
            assert func(args).to_dict() == args[0].to_dict()
        else:
            assert_binary_op(name, func(args), *args)


def test_if():
    x = cc.column("a") > cc.literal(2)
    y = cc.column("b")
    z = cc.column("c")
    i = cc.if_(x, y, z)
    assert_if_op(i, x, y, z)

    with pytest.raises(TypeError):
        cc.if_(x, y, 2.0)

    with pytest.raises(TypeError):
        cc.if_(x, "a", z)

    with pytest.raises(TypeError):
        cc.if_(True, y, z)

    with pytest.raises(TypeError):
        j = cc.if_(x, y, {"lit": [2.0]})


def test_immutable():
    val = cc.column("a")
    with pytest.raises(TypeError):
        val["test"] = 2.0

    with pytest.raises(TypeError):
        val.update({"test": 2.0})

    with pytest.raises(TypeError):
        val.pop("ref")

    with pytest.raises(TypeError):
        val.popitem()

    with pytest.raises(TypeError):
        val.setdefault("a", None)

    with pytest.raises(TypeError):
        del val["val"]


def test_static_constructors():
    x1 = CCE.col("2")
    x2 = CCE.col({"ref": ["2"]})
    x3 = CCE.col(2)
    assert x1.to_dict() == x2.to_dict() == x3.to_dict()

    with pytest.raises(ValueError):
        CCE.col({"lit": [2.0]})

    y1 = CCE.lit(2.0)
    y2 = CCE.lit({"lit": [2.0]})
    y3 = CCE.lit(2)
    assert y1.to_dict() == y2.to_dict() == y3.to_dict()

    with pytest.raises(ValueError):
        CCE.lit({"ref": ["2"]})


def test_constants():
    e1 = cc.e
    e2 = CCE({"const": ["e"]})
    e3 = CCE.const("e")
    assert e1.to_dict() == e2.to_dict() == e3.to_dict()

    p1 = cc.pi
    p2 = CCE({"const": ["pi"]})
    p3 = CCE.const("pi")
    assert p1.to_dict() == p2.to_dict() == p3.to_dict()

    n1 = cc.nan
    n2 = CCE({"const": ["nan"]})
    n3 = CCE.const("nan")
    assert n1.to_dict() == n2.to_dict() == n3.to_dict()
