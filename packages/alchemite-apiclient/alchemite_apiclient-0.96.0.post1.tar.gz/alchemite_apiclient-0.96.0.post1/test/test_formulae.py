import pytest

from alchemite_apiclient.calculated_columns import formulae


@pytest.mark.parametrize("constant", [None, 2.0])
def test_col_sum(constant):
    truth = {"sum": [{"ref": ["a"]}, {"ref": ["b"]}, {"ref": ["c"]}]}
    if constant is not None:
        truth = {"+": [truth, {"lit": [constant]}]}
    test = formulae.col_sum(["a", "b", "c"], constant)
    assert truth == test.to_dict()


def test_col_mean():
    truth = {"avg": [{"ref": ["a"]}, {"ref": ["b"]}, {"ref": ["c"]}]}
    test = formulae.col_mean(["a", "b", "c"])
    assert truth == test.to_dict()


def test_col_ratio():
    truth = {"/": [{"ref": ["a"]}, {"ref": ["b"]}]}
    test = formulae.col_ratio("a", "b")
    assert truth == test.to_dict()


@pytest.mark.parametrize("constant", [None, 2.0])
def test_weighted_sum(constant):
    truth = {"sum": [{"*": [{"ref": ["a"]}, {"lit": [3.0]}]},
                     {"*": [{"ref": ["b"]}, {"lit": [2.0]}]},
                     {"*": [{"ref": ["c"]}, {"lit": [1.0]}]}]}
    if constant is not None:
        truth = {"+": [truth, {"lit": [constant]}]}
    test = formulae.weighted_sum(["a", "b", "c"], [3.0, 2.0, 1.0], constant)
    assert truth == test.to_dict()


def test_weighted_mean():
    truth = {"/": [{"sum": [{"*": [{"ref": ["a"]}, {"lit": [3.0]}]},
                            {"*": [{"ref": ["b"]}, {"lit": [2.0]}]},
                            {"*": [{"ref": ["c"]}, {"lit": [1.0]}]}]}, {"lit": [6.0]}]}
    test = formulae.weighted_mean(["a", "b", "c"], [3.0, 2.0, 1.0])
    assert truth == test.to_dict()


def test_weighted_col_sum():
    truth = {"sum": [{"*": [{"ref": ["a"]}, {"ref": ["d"]}]},
                     {"*": [{"ref": ["b"]}, {"ref": ["e"]}]},
                     {"*": [{"ref": ["c"]}, {"ref": ["f"]}]}]}
    test = formulae.weighted_col_sum(["a", "b", "c"], ["d", "e", "f"])
    assert truth == test.to_dict()


def test_weighted_inverse_col_sum():
    truth = {"sum": [{"/": [{"ref": ["a"]}, {"ref": ["d"]}]},
                     {"/": [{"ref": ["b"]}, {"ref": ["e"]}]},
                     {"/": [{"ref": ["c"]}, {"ref": ["f"]}]}]}
    test = formulae.weighted_inverse_col_sum(["a", "b", "c"], ["d", "e", "f"])
    assert truth == test.to_dict()


def test_weighted_col_mean():
    truth = {"/": [{"sum": [{"*": [{"ref": ["a"]}, {"ref": ["d"]}]},
                            {"*": [{"ref": ["b"]}, {"ref": ["e"]}]},
                            {"*": [{"ref": ["c"]}, {"ref": ["f"]}]}]},
                   {"sum": [{"ref": ["d"]},
                            {"ref": ["e"]},
                            {"ref": ["f"]}]}]}
    test = formulae.weighted_col_mean(["a", "b", "c"], ["d", "e", "f"])
    assert truth == test.to_dict()


@pytest.mark.parametrize("weight", [None, 2.0])
def test_col_product(weight):
    truth = {"product": [{"ref": ["a"]}, {"ref": ["b"]}, {"ref": ["c"]}]}
    if weight is not None:
        truth = {"*": [truth, {"lit": [weight]}]}
    test = formulae.col_product(["a", "b", "c"], weight)
    assert truth == test.to_dict()


def test_weighted_ratio():
    truth = {"/": [{"sum": [{"*": [{"ref": ["a"]}, {"lit": [6.0]}]},
                            {"*": [{"ref": ["b"]}, {"lit": [5.0]}]},
                            {"*": [{"ref": ["c"]}, {"lit": [4.0]}]}]},
                   {"sum": [{"*": [{"ref": ["d"]}, {"lit": [3.0]}]},
                            {"*": [{"ref": ["e"]}, {"lit": [2.0]}]},
                            {"*": [{"ref": ["f"]}, {"lit": [1.0]}]}]}]}
    test = formulae.weighted_ratio(["a", "b", "c"], [6.0, 5.0, 4.0],
                                   ["d", "e", "f"], [3.0, 2.0, 1.0])
    assert truth == test.to_dict()
