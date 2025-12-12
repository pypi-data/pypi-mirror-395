"""
Some useful higher level functions to assist with creating common calculated columns
"""

from typing import List, Optional

from alchemite_apiclient.calculated_columns.helpers import (
    CalculatedColumnExpression as _CCE,
)
from alchemite_apiclient.calculated_columns.helpers import (
    column,
    literal,
    mean,
    product,
    sum_,
)


def col_sum(cols: List[str], constant: Optional[float] = None) -> _CCE:
    """
    Sum up the values in the specified columns, optionally also adding a constant.

    Args:
        cols: List of column names to sum
        constant: an optional constant value to add

    Returns: CalculatedColumnExpression
    """

    if constant is None:
        return sum_([column(i) for i in cols])
    else:
        return sum_([column(i) for i in cols]) + literal(constant)


def col_mean(cols: List[str]) -> _CCE:
    """
    Take the mean of the specified columns.

    Args:
        cols: List of column names to average

    Returns: CalculatedColumnExpression
    """
    return mean([column(i) for i in cols])


def col_ratio(numerator: str, denominator: str) -> _CCE:
    """
    Calculates the ratio of two columns.

    Args:
        numerator: Column name to form numerator of the ratio
        denominator: Column name to form denominator of the ratio

    Returns:

    """
    return column(numerator) / column(denominator)


def weighted_sum(
    cols: List[str], weights: List[float], constant: Optional[float] = None
) -> _CCE:
    """
    Sum up the values in the specified columns, multiplied by the corresponding weight.

    Args:
        cols: List of column names to sum
        weights: List of weights to multiply each column by
        constant: an optional constant value to add to the final result

    Returns: CalculatedColumnExpression
    """
    if constant is None:
        return sum_([column(i) * literal(j) for i, j in zip(cols, weights)])
    else:
        return sum_(
            [column(i) * literal(j) for i, j in zip(cols, weights)]
        ) + literal(constant)


def weighted_mean(cols: List[str], weights: List[float]) -> _CCE:
    """
    Take the weighted mean of the specified columns using the corresponding weights.

    Args:
        cols: List of column names to average
        weights: List of weights to multiply each column by

    Returns: CalculatedColumnExpression
    """
    return sum_(
        [column(i) * literal(j) for i, j in zip(cols, weights)]
    ) / literal(sum(weights))


def weighted_col_sum(summand_cols: List[str], weight_cols: List[str]) -> _CCE:
    """
    Use the values in the columns called weights to weight the sum of the columns in summands.

    Args:
        summand_cols: List of column names to sum
        weight_cols: List of columns names to multiply each summand column by

    Returns: CalculatedColumnExpression
    """
    return sum_(
        [column(i) * column(j) for i, j in zip(summand_cols, weight_cols)]
    )


def weighted_inverse_col_sum(
    summand_cols: List[str], weight_cols: List[str]
) -> _CCE:
    """
    Use the inverse of the values in the columns called weights to weight the sum of the columns in summands.

    Args:
        summand_cols: List of column names to sum
        weight_cols: List of columns names to divide each summand column by

    Returns: CalculatedColumnExpression
    """
    return sum_(
        [column(i) / column(j) for i, j in zip(summand_cols, weight_cols)]
    )


def weighted_col_mean(summand_cols: List[str], weight_cols: List[str]) -> _CCE:
    """
    Use the values in the columns called weights to weight the mean of the columns in summands.

    Args:
        summand_cols: List of column names to average
        weight_cols: List of columns names to multiply each summand column by

    Returns: CalculatedColumnExpression
    """
    return sum_(
        [column(i) * column(j) for i, j in zip(summand_cols, weight_cols)]
    ) / sum_([column(j) for j in weight_cols])


def col_product(cols: List[str], weight: Optional[float] = None) -> _CCE:
    """
    Take the product of the values in the columns, optionally also multiplying by a constant.

    Args:
        cols: List of column names to multiply together
        weight: an optional additional constant value to multiply by

    Returns: CalculatedColumnExpression
    """
    if weight is None:
        return product([column(i) for i in cols])
    else:
        return product([column(i) for i in cols]) * weight


def weighted_ratio(
    numerator_cols: List[str],
    numerator_weights: List[float],
    denominator_cols: List[str],
    denominator_weights: List[float],
) -> _CCE:
    """
    Calculate the weighted sum of the numerator columns, weighted by the numerator weights,
        then divide this by the corresponding denominator weighted sum.

    Args:
        numerator_cols: List of column names to sum together for the numerator
        numerator_weights: List of weights to multiply each column in the numerator by
        denominator_cols: List of column names to sum together for the denominator
        denominator_weights: List of weights to multiply each column in the denominator by

    Returns: CalculatedColumnExpression
    """
    numer = weighted_sum(numerator_cols, numerator_weights)
    denom = weighted_sum(denominator_cols, denominator_weights)
    return numer / denom
