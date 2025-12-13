from xcdo import DatasetIn, DatasetOut

from . import operator


@operator()
def mermean(
    input: DatasetIn,
) -> DatasetOut:
    """
    Meridional mean

    operator examples:
        xcdo -meremean infile.nc outfile.nc
    """
    return input.cf.mean("longitude")  # type: ignore


@operator()
def mermin(
    input: DatasetIn,
) -> DatasetOut:
    """
    Meridional minimum

    operator examples:
        xcdo -mermin infile.nc outfile.nc
    """
    return input.cf.min("longitude")  # type: ignore


@operator()
def mermax(
    input: DatasetIn,
) -> DatasetOut:
    """
    Meridional maximum

    operator examples:
        xcdo -mermax infile.nc outfile.nc
    """
    return input.cf.max("longitude")  # type: ignore


@operator()
def merstd(
    input: DatasetIn,
) -> DatasetOut:
    """
    Meridional standard deviation

    operator examples:
        xcdo -merstd infile.nc outfile.nc
    """
    return input.cf.std("longitude")  # type: ignore


@operator()
def mersum(
    input: DatasetIn,
) -> DatasetOut:
    """
    Meridional sum

    operator examples:
        xcdo -mersum infile.nc outfile.nc
    """
    return input.cf.sum("longitude")  # type: ignore
