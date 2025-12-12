import os
import shutil
import subprocess
import tempfile

from xcdo import XcdoError
from xcdo import xarray as xr
from xcdo.io_utils import open_dataset

from . import operator


@operator(name="cdo", implicit="input", is_delegate=True)
def cdo_run(*arguments: str) -> xr.Dataset:
    """
    Operator to run CDO commands

    description:
        This operator is a delegate to the CDO command line tool. It takes a list of CDO arguments and runs the CDO command with those arguments.
        The CDO executable is found using the 'CDO' environment variable, or defaults to "cdo" from the path.
        It only support cdo commands that outputs a single file.
        Note: The given arguments should not include the output file name.

    operator example:
        xcdo -plot -cdo -timmean input.nc
        xcdo -print -cdo [ -ymonmean -mergetime input1.nc input2.nc ]
    """
    # Use CDO env variable path to find the CDO executable
    cdo_path = os.environ.get("CDO", "cdo")
    # Check if CDO is installed
    if not shutil.which(cdo_path):
        raise XcdoError("cdo executable not found!")

    with tempfile.NamedTemporaryFile(suffix=".nc") as tmp:
        subprocess.check_call([cdo_path, "-f", "nc", *arguments, tmp.name])
        return open_dataset(tmp.name)
