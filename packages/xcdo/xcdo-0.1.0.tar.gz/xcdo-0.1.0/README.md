
# XCDO

![Test](https://github.com/prajeeshag/xcdo/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/prajeeshag/xcdo/graph/badge.svg?token=UNNUW30IQL)](https://codecov.io/gh/prajeeshag/xcdo)
![PyPI - Version](https://img.shields.io/pypi/v/xcdo)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/clios)
![Doc](https://github.com/prajeeshag/xcdo/actions/workflows/build-docs.yml/badge.svg)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)


**XCDO** is a Python-based command-line tool built around [Xarray](https://docs.xarray.dev/en/stable/). It provides a collection of operators for working with datasets such as NetCDF, GRIB, and Zarr, using a familiar [CDO](https://code.mpimet.mpg.de/projects/cdo/)-style interface. With the help of Python’s type annotations, creating new operators becomes effortless, making it easy to extend the tool with simple functions and build reusable, organised analysis workflows.

## Installation
```bash
$ pip install xcdo
```
<br>
You may want to install `xcdo` to an isolated virtual environment to avoid conflicts with other packages.
Below are examples using common environment managers:

### [micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html)/[mamba](https://mamba.readthedocs.io/en/latest/)/[conda](https://docs.conda.io/en/latest/)

```bash
# Choose any of: micromamba, mamba, or conda
$ micromamba create -n xcdo python=3.13
$ micromamba activate xcdo
(xcdo)$ pip install xcdo
```

### [uv](https://docs.astral.sh/uv/)

```bash
$ uv venv --python 3.13 .venv
$ source .venv/bin/activate
(.venv)$ pip install xcdo
```

## Usage

Generally, XCDO works much like [CDO](https://code.mpimet.mpg.de/projects/cdo/wiki). For example:
```bash
$ xcdo -selvar,var1 indata.nc outdata.nc
$ xcdo -timemean -zonmean in.nc out.nc
```
<br>

You can find a list of all available operators [here](operators/index.md).
or run `xcdo --list` on the command line.
```bash
$ xcdo --list

                            Available Operators
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Operator      ┃ Description                                   ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ cdo           │ Operator to run CDO commands                  │
│ showtimestamp │ Show time stamp                               │
│ mermean       │ Meridional mean                               │
│ mermin        │ Meridional minimum                            │
│ mermax        │ Meridional maximum                            │
│ merstd        │ Meridional standard deviation                 │
│ mersum        │ Meridional sum                                │
```
<br>

To get detailed information and the synopsis (or signature) about a specific operator, use:
```bash
$ xcdo --show <operator>
```
```bash
$ xcdo --show selvar
╭─ Synopsis ──────────────────────────────────────────────────╮
│                                                             │
│  xcdo -selvar,name input output                             │
│                                                             │
╰─────────────────────────────────────────────────────────────╯
╭─ Description ───────────────────────────────────────────────╮
│                                                             │
│  Select a data variable by name.                            │
│                                                             │
╰─────────────────────────────────────────────────────────────╯
                 Positional Arguments
┏━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃ Parameter ┃ Type ┃ Required ┃ Description          ┃
┡━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ name      │ TEXT │ Required │ Name of the variable │
└───────────┴──────┴──────────┴──────────────────────┘
╭─ Examples ──────────────────────────────────────────────────╮
│                                                             │
│  xcdo -selvar,tas infile.nc outfile.nc                      │
│  xcdo -selname,tas infile.nc outfile.nc                     │
│                                                             │
╰─────────────────────────────────────────────────────────────╯
```
<br>

## User-defined operators
You can easily turn a regular Python function into your own XCDO operator. For example, here’s a small operator in a file named dump.py that simply prints a dataset to the terminal:

```py title="dump.py"
# dump.py
from xcdo import operator, DatasetIn

@operator()
def main(input: DatasetIn):
    print(input)
```

And this can be used as follows in `xcdo`:

```bash
$ xcdo -dump.py in.nc
```
You can see the signature and documentation of the custom operator by running:

```bash
$ xcdo --show dump.py

╭─ Synopsis ──────────────────────────────────────────────────╮
│                                                             │
│  xcdo -dump.py input                                        │
│                                                             │
╰─────────────────────────────────────────────────────────────╯

```
!!! Note
    Notice the `.py` extension on the custom operator? That’s because the operator name simply comes from the Python file’s name.

See [Writing your own operators](user_defined_operators.md) for more details.

## Why XCDO?
- **Simple Python functions**. If you know Python, you can create new operators instantly. This opens the door for real community-driven development.
- **Automatic help and documentation**. XCDO automatically generates help and documentation for your operators, making it easy to share and reuse them.
- **CLI and Library**. As these operators are Python functions, it can be called from Python scripts as well.
- **Custom operators**. Drop a Python function into a file and call it like any other XCDO operator. This keeps your analysis workflows clean, modular, and easy to reuse.
- **Zarr support**. Since XCDO builds on Xarray, it naturally supports modern formats like Zarr, which CDO doesn’t handle yet.
- **CDO integration**. When you need the performance of CDO, you can call it directly with the “-cdo” operator and combine it with XCDO or custom operators in one chain.


With community support, XCDO can grow into a unified library of reusable and well-structured tools for climate and weather analysis.


## Issues
Please report any issues [here](https://github.com/prajeeshag/xcdo/issues).

## Contributing
Fork the [repository](https://github.com/prajeeshag/xcdo) and make your changes and submit a pull request.

Please contact me at [prajeeshag@gmail.com](mailto:prajeeshag@gmail.com) for any questions or start a discussion on [GitHub Discussions](https://github.com/prajeeshag/xcdo/discussions).

!!! warning "Under active development"
    XCDO is under active development. Although everything will work as expected, many features are not documented well yet.

<!--For a more complete example including more features, see the Tutorial - User Guide.-->
