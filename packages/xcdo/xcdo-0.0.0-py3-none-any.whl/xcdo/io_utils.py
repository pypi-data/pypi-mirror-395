import xarray as xr


def _guess_engine(path: str) -> str | None:
    grib_extensions = [".grib", ".grib1", ".grb", ".grb1", ".grib2", ".grb2"]
    zarr_extensions = [".zarr", ".zip"]
    for ext in grib_extensions:
        if path.endswith(ext):
            return "cfgrib"
    for ext in zarr_extensions:
        if path.endswith(ext):
            return "zarr"
    return None


def _guess_output_format(path: str) -> str:
    """Guess the output format based on the file extension"""
    if path.endswith(".zarr") or path.endswith(".zip"):
        return "zarr"
    return "netcdf"


def open_dataset(path: str) -> xr.Dataset:
    engine = _guess_engine(path)
    return xr.open_dataset(  # pyright: ignore
        path,
        chunks={},
        engine=engine,
    )


def save_dataset(dataset: xr.Dataset, path: str) -> None:
    format = _guess_output_format(path)
    if format == "zarr":
        dataset.to_zarr(path, mode="w")  # pyright: ignore
        return
    dataset.to_netcdf(path)  # pyright: ignore
