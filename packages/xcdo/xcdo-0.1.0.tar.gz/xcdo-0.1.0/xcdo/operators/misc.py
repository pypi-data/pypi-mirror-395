import typing as t

import numpy as np
import rich

from xcdo import DatasetIn, DatasetOut, Doc, XcdoError
from xcdo import xarray as xr

from . import operator


@operator(name="print")
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
    rich.print(input)  # pragma: no cover


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


@operator()
def setchunk(
    inputs: DatasetIn,
    **chunks: t.Annotated[
        int, Doc("Chunk size for each dimension, e.g. -setchunk,time=10,lon=20")
    ],
) -> DatasetOut:
    """
    Set the chunk size of a dataset.

    description:
        Use xarray's `chunk` method to set the chunk size of a dataset.
        Refer to xarray's documentation for more information:
        https://docs.xarray.dev/en/stable/generated/xarray.Dataset.chunk.html

    operator examples:
        xcdo -setchunk,time=10 infile.nc outfile.nc
        xcdo -setchunk,time=10,lon=20,lat=10 infile.nc outfile.nc
    """
    try:
        return inputs.chunk(chunks)
    except ValueError as e:
        raise XcdoError(str(e))


@operator(name="float2int16")
@operator()
def float2short(input: DatasetIn) -> DatasetOut:
    """
    Convert float variables to int16

    description:
        This operator converts all float variables in the given dataset to int16 (short).
        Note: Conversion happens only when the dataset is written to disk.

    operator examples:
        xcdo -float2short infile.nc outfile.nc
    """
    out = input.copy()
    for var in out.data_vars:
        da = out[var]
        if da.dtype not in (np.float32, np.float64):
            continue  # pragma: no cover

        # ignore NaNs in scaling
        vmin = float(np.nanmin(da.values))
        vmax = float(np.nanmax(da.values))

        info = np.iinfo(np.int16)
        max_range = info.max - info.min

        if (vmax - vmin) > max_range:
            raise XcdoError(
                f"Variable '{var}' range [{vmin}, {vmax}] too large for int16."
            )

        scale_factor = (vmax - vmin) / max_range
        add_offset = vmin - scale_factor * info.min
        fill = np.int16(-32767)

        # write encoding (THIS controls final disk storage)
        out[var].encoding.update(
            {
                "dtype": np.int16,
                "scale_factor": scale_factor,
                "add_offset": add_offset,
                "_FillValue": fill,
                "missing_value": fill,
            }
        )
        if "missing_value" in out[var].attrs:
            del out[var].attrs["missing_value"]
        if "_FillValue" in out[var].attrs:
            del out[var].attrs["_FillValue"]

    return out
