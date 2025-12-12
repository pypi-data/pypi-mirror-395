import typing as t

import numpy as np
import xarray as xr
from typing_extensions import Doc

from xcdo import DatasetIn, DatasetOut, FloatParam, IntParam, StrParam, XcdoError

from . import operator


@operator(name="selname")
@operator()
def selvar(
    input: DatasetIn,
    name: t.Annotated[StrParam, Doc("Name of the variable")],
) -> DatasetOut:
    """
    Select a data variable by name.

    operator examples:
        xcdo -selvar,tas infile.nc outfile.nc
        xcdo -selname,tas infile.nc outfile.nc
    """
    try:
        return input.data_vars[name].to_dataset()
    except KeyError:
        raise XcdoError(
            f"`{name}` is not a data variable! Available data variables: {input.data_vars}"
        )


@operator(name="isel")
def isel(
    input: DatasetIn, **indexes: t.Annotated[IntParam, Doc("Indexes to select")]
) -> DatasetOut:
    """
    Index along specified dimensions.

    description:
        Use xarray's `isel` method to return a new dataset with each array indexed along the specified dimension(s).

    operator examples:
        xcdo -isel,time=0,lon=100 infile.nc outfile.nc
    """
    return input.isel(
        indexes,
    )


def _sellonlatbox_curvilinear(
    ds: DatasetIn, wlon: float, elon: float, slat: float, nlat: float
) -> DatasetOut:
    lon_name, lat_name = (
        ds.cf.coordinates["longitude"][0],
        ds.cf.coordinates["latitude"][0],
    )
    lon = ds[lon_name]
    lat = ds[lat_name]
    mask = (lon >= wlon) & (lon <= elon) & (lat >= slat) & (lat <= nlat)
    if not mask.any():
        raise XcdoError("Selection is empty")
    # Get the indices of all True values
    y_idx, x_idx = np.where(mask.values)
    # Rectangular bounding box in index space
    ymin, ymax = y_idx.min(), y_idx.max()
    xmin, xmax = x_idx.min(), x_idx.max()
    yname, xname = lon.dims
    return ds.isel({yname: slice(ymin, ymax + 1), xname: slice(xmin, xmax + 1)})


@operator()
def sellonlatbox(
    input: DatasetIn,
    wlon: t.Annotated[FloatParam, Doc("Western longitude")],
    elon: t.Annotated[FloatParam, Doc("Eastern longitude")],
    slat: t.Annotated[FloatParam, Doc("Southern latitude")],
    nlat: t.Annotated[FloatParam, Doc("Northern latitude")],
) -> DatasetOut:
    """
    Select a region using the longitude and latitude bounds.

    description:
        Selects a region using the longitude and latitude bounds.
        If the input data is in [-180, 180] format, and is asked to select the region from 0 to 360,
        it will take care of the wrapping and vice versa.

        The longitude should be in the range of [-180, 180] or [0, 360].
        The latitude should be in the range of [-90, 90].
        The western longitude should be smaller than the eastern longitude.
        The southern latitude should be smaller than the northern latitude.


    operator examples:
        xcdo -sellonlatbox,-10,50,-50,60 infile.nc outfile.nc
    """
    if wlon > elon:
        raise XcdoError("Western longitude should be smaller than Eastern longitude")
    if slat > nlat:
        raise XcdoError("Southern latitude should be smaller than Northern latitude")
    if wlon < -180:
        raise XcdoError("Western longitude should be larger than -180")
    if elon > 360:
        raise XcdoError("Eastern longitude should be smaller than 360")
    if slat < -90:
        raise XcdoError("Southern latitude should be larger than -90")
    if nlat > 90:
        raise XcdoError("Northern latitude should be smaller than 90")
    if wlon < 0 and elon > 180:
        raise XcdoError("Longitude should be either [-180, 180] or [0, 360] format")

    if "longitude" not in input.cf.coordinates:
        raise XcdoError("Longitude not found in coordinates")

    if "latitude" not in input.cf.coordinates:
        raise XcdoError("Latitude not found in coordinates")

    if (
        len(input.cf.coordinates["longitude"]) != 1
        or len(input.cf.coordinates["latitude"]) != 1
    ):
        raise XcdoError("Cannot handle selection for datasets with multiple grids")

    lon_name, lat_name = (
        input.cf.coordinates["longitude"][0],
        input.cf.coordinates["latitude"][0],
    )

    lon = input[lon_name]

    if len(lon.shape) > 1:
        return _sellonlatbox_curvilinear(input, wlon, elon, slat, nlat)

    min_lon = float(lon.min())
    max_lon = float(lon.max())

    is_0360 = min_lon >= 0 and max_lon <= 360

    flip = False
    if is_0360:
        if wlon < 0:
            flip = True
            wlon = wlon + 360
        if elon < 0:
            flip = True
            elon = elon + 360
    else:
        if wlon > 180:
            flip = True
            wlon = ((wlon + 180) % 360) - 180
        if elon > 180:
            flip = True
            elon = ((elon + 180) % 360) - 180

    if wlon > elon:
        part1 = input.sel({lon_name: slice(wlon, max_lon), lat_name: slice(slat, nlat)})
        part2 = input.sel({lon_name: slice(min_lon, elon), lat_name: slice(slat, nlat)})
        if is_0360:
            part1 = part1.assign_coords({lon_name: part1[lon_name] - 360.0})
        else:
            part2 = part2.assign_coords({lon_name: part2[lon_name] + 360.0})
        return xr.concat([part1, part2], dim=lon_name)
    else:
        part = input.sel({lon_name: slice(wlon, elon), lat_name: slice(slat, nlat)})
        if flip:
            if is_0360:
                part = part.assign_coords({lon_name: part[lon_name] - 360.0})
            else:
                part = part.assign_coords({lon_name: part[lon_name] + 360.0})
        return part
