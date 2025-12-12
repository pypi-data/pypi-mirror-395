import typing as t

from typing_extensions import Doc

from xcdo import DatasetIn, DatasetOut, StrParam

from . import operator


@operator()
def renamedim(
    input: DatasetIn,
    oldname: t.Annotated[StrParam, Doc("Old name of the dimension")],
    newname: t.Annotated[StrParam, Doc("New name of the dimension")],
) -> DatasetOut:
    """
    Rename a dimension in a dataset.

    operator examples:
        xcdo -renamedim,lon,longitude infile.nc outfile.nc
    """
    return input.rename_dims({oldname: newname})


@operator()
def rename(
    input: DatasetIn,
    oldname: t.Annotated[StrParam, Doc("Old name of the variable")],
    newname: t.Annotated[StrParam, Doc("New name of the variable")],
) -> DatasetOut:
    """
    Rename a variable in a dataset.

    operator examples:
        xcdo -rename,lon,longitude infile.nc outfile.nc
        xcdo -rename,tas,temp infile.nc outfile.nc
    """
    return input.rename_vars({oldname: newname})
