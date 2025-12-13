from xcdo import DatasetIn, XcdoError

from . import operator


@operator()
def showtimestamp(
    input: DatasetIn,
) -> None:
    """
    Show time stamp

    operator examples:
        xcdo -showtimestamp infile.nc
    """

    try:
        time_coord = input.cf["time"]
    except KeyError:
        raise XcdoError("No 'time' coordinate found in the dataset")

    print(time_coord.values)  # noqa: T201
