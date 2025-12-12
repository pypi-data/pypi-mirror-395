from xcdo import DatasetIn, DatasetOut

from . import operator


@operator()
def timemean(
    input: DatasetIn,
) -> DatasetOut:
    """
    Mean over all timesteps

    operator examples:
        xcdo -timemean infile.nc outfile.nc
    """
    return input.cf.mean("time")  # type: ignore


@operator()
def timemin(
    input: DatasetIn,
) -> DatasetOut:
    """
    Minimum value over all timesteps

    operator examples:
        xcdo -timemin infile.nc outfile.nc
    """
    return input.cf.min("time")  # type: ignore


@operator()
def timemax(
    input: DatasetIn,
) -> DatasetOut:
    """
    Maximum value over all timesteps

    operator examples:
        xcdo -timemax infile.nc outfile.nc
    """
    return input.cf.max("time")  # type: ignore


@operator()
def timestd(
    input: DatasetIn,
) -> DatasetOut:
    """
    Standard deviation over all timesteps

    operator examples:
        xcdo -timestd infile.nc outfile.nc
    """
    return input.cf.std("time")  # type: ignore


@operator()
def timesum(
    input: DatasetIn,
) -> DatasetOut:
    """
    Sum over all timesteps

    operator examples:
        xcdo -timesum infile.nc outfile.nc
    """
    return input.cf.sum("time")  # type: ignore
