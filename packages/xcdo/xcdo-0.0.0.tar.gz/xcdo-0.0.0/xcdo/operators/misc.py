import typing as t

import rich

from xcdo import DatasetIn, DatasetOut
from xcdo import xarray as xr

from . import operator


@operator(implicit="param", name="print")
def print_dataset(input: DatasetIn) -> None:
    """
    Simply print the given dataset.

    description:
        This operator simply prints the given dataset to the terminal.
        It uses `rich` library to display the dataset in a more readable format.

    operator examples:
        xcdo -print infile.nc
        xcdo -print -selvar,var infile.nc
    """
    rich.print(input)


@operator(implicit="param")
def merge(
    *inputs: DatasetIn,
    compat: t.Literal[
        "identical", "equals", "broadcast_equals", "no_conflicts", "override", "minimal"
    ] = "no_conflicts",
    join: t.Literal["outer", "inner", "left", "right", "exact", "override"] = "outer",
    combine_attrs: t.Literal[
        "drop", "identical", "no_conflicts", "override"
    ] = "override",
) -> DatasetOut:
    """
    Merge multiple datasets into one.

    description:
        Use xarray's `merge` method to merge multiple datasets into one.
        Refer to xarray's documentation for more information regarding the options:
        https://docs.xarray.dev/en/stable/generated/xarray.merge.html

    operator examples:
        xcdo -merge infile1.nc infile2.nc infile2.nc outfile.nc
    """
    return xr.merge(inputs, compat=compat, join=join, combine_attrs=combine_attrs)
