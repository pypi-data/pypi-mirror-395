import cf_xarray as cf_xarray
import xarray as xarray

from .exceptions import XcdoError


@xarray.register_dataset_accessor("get_dataarray")  # type: ignore
class GetDataArray:
    def __init__(self, dataset: xarray.Dataset):
        self._dataset = dataset

    def __call__(self) -> xarray.DataArray:
        """
        Get a DataArray from a Dataset

        if the Dataset has only one data variable, return that variable as a DataArray

        Raises:
            XcdoError: if the Dataset has multiple data variables
        """
        if len(self._dataset.data_vars) > 1:
            raise XcdoError(
                f"Dataset should have a single data variable, Got {self._dataset.data_vars}"
            )
        elif len(self._dataset.data_vars) == 0:
            raise XcdoError("No data variables found")

        da_name: str = list(self._dataset.data_vars)[0]
        return self._dataset[da_name]


custom_criteria = {
    "time": {
        "name": "Time|time|times|Times",
    }
}
cf_xarray.set_options(custom_criteria=custom_criteria)  # type: ignore
