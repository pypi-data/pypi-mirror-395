import enum
import typing as t

from typing_extensions import Doc

from xcdo import DatasetIn, DatasetOut, FloatParam, Param, XcdoError

from . import operator


class SetMissExpr(enum.StrEnum):
    eq = "eq"
    gt = "gt"
    lt = "lt"
    ge = "ge"
    le = "le"


SetMissExprType = t.Annotated[
    SetMissExpr,
    Param(),
    Doc("Expression to set missing values."),
]


@operator()
def settomiss(
    input: DatasetIn,
    value: t.Annotated[FloatParam, Doc("")],
    expr: SetMissExprType = SetMissExpr.eq,
) -> DatasetOut:
    """
    Set values in a dataset to missing values.

    description:
        Set values in a dataset to missing values based on the given expression.
        For example, if the expression is `gt` (greater than), then all points with values greater than the given value will be set to missing.
        Default expression is `eq` (equal to).

    operator examples:
        xcdo -settomiss,0 infile.nc outfile.nc
        xcdo -settomiss,5,gt infile.nc outfile.nc
    """
    match expr:
        case SetMissExpr.eq:
            for var in input.data_vars:
                input[var] = input[var].where(input[var] != value)
        case SetMissExpr.gt:
            for var in input.data_vars:
                input[var] = input[var].where(input[var] <= value)
        case SetMissExpr.lt:
            for var in input.data_vars:
                input[var] = input[var].where(input[var] >= value)
        case SetMissExpr.ge:
            for var in input.data_vars:
                input[var] = input[var].where(input[var] < value)
        case SetMissExpr.le:
            for var in input.data_vars:
                input[var] = input[var].where(input[var] > value)
        case _:
            raise XcdoError(f"Unknown expression: {expr}")
    return input
