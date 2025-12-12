from xcdo import DatasetIn, DatasetOut

from . import operator


@operator()
def zonmean(
    input: DatasetIn,
) -> DatasetOut:
    """
    Zonal mean

    operator examples:
        xcdo -zonemean infile.nc outfile.nc
    """
    return input.cf.mean("latitude")  # type: ignore


@operator()
def zonmin(
    input: DatasetIn,
) -> DatasetOut:
    """
    Zonal minimum

    operator examples:
        xcdo -zonmin infile.nc outfile.nc
    """
    return input.cf.min("latitude")  # type: ignore


@operator()
def zonmax(
    input: DatasetIn,
) -> DatasetOut:
    """
    Zonal maximum

    operator examples:
        xcdo -zonmax infile.nc outfile.nc
    """
    return input.cf.max("latitude")  # type: ignore


@operator()
def zonstd(
    input: DatasetIn,
) -> DatasetOut:
    """
    Zonal standard deviation

    operator examples:
        xcdo -zonstd infile.nc outfile.nc
    """
    return input.cf.std("latitude")  # type: ignore


@operator()
def zonsum(
    input: DatasetIn,
) -> DatasetOut:
    """
    Zonal sum

    operator examples:
        xcdo -zonsum infile.nc outfile.nc
    """
    return input.cf.sum("latitude")  # type: ignore
