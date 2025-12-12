from xcdo import DatasetIn
from xcdo.exceptions import XcdoError

from . import operator


@operator()
def plot(input: DatasetIn) -> None:
    """
    A simple plot function for xarray DataArray.

    description:
        This function uses xarray.DataArray's `plot` method to plot the given dataset.
        It opens a interactive matplotlib window.

    operator examples:
        xcdo -plot infile.nc
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise XcdoError("`matplotlib` is not installed")
    darray = input.get_dataarray()
    darray.plot()
    plt.show()
