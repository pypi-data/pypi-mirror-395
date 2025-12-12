
# XCDO

![Test](https://github.com/prajeeshag/xcdo/actions/workflows/test.yml/badge.svg)
![Doc](https://github.com/prajeeshag/xcdo/actions/workflows/build-docs.yml/badge.svg)
![PyPI - Version](https://img.shields.io/pypi/v/xcdo)
[![codecov](https://codecov.io/gh/prajeeshag/xcdo/graph/badge.svg?token=UNNUW30IQL)](https://codecov.io/gh/prajeeshag/xcdo)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

**XCDO** is a Python-based command-line tool built around [Xarray](https://docs.xarray.dev/en/stable/). It provides a collection of operators for working with datasets such as NetCDF, GRIB, and Zarr, using a familiar [CDO](https://code.mpimet.mpg.de/projects/cdo/)-style interface. With the help of Python’s type annotations, creating new operators becomes effortless, making it easy to extend the tool with simple functions and build reusable, organised analysis workflows.

## Why XCDO?
Why build another CDO-style tool—even if it won’t be as fast as the original CDO? Because XCDO offers a different kind of power:

- Write operators as simple Python functions. If you know Python, you can create new operators instantly. This opens the door for real community-driven development.
- As these operators are Python functions, it can be called from Python scripts as well.
- Use your own code as operators. Drop a Python function into a file and call it like any other XCDO operator. This keeps workflows clean, modular, and easy to reuse.
- Full Zarr support. Since XCDO builds on Xarray, it naturally supports modern formats like Zarr, which CDO doesn’t handle yet.
- Smooth CDO integration. When you need the performance of CDO, you can call it directly with the “-cdo” operator and combine it with XCDO or custom operators in one chain.

With community support, XCDO can grow into a unified library of reusable and well-structured tools for climate and weather analysis.


## Installation
<!--termynal-->
```
$ pip install xcdo
```

You may want to install `xcdo` to an isolated virtual environment to avoid conflicts with other packages. Use any virtual environment manager such as [micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html) or [conda](https://docs.conda.io/en/latest/) or [virtualenv](https://virtualenv.pypa.io/en/latest/) or [venv](https://docs.python.org/3/library/venv.html)

Optionaly, you may also install `cdo` for using the `-cdo`.

## Usage
To get a list of all available operators and their short descriptions, use:

```bash
$ xcdo --list
```

<!--termynal--->
```
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


To get detailed information and the synopsis (or signature) about a specific operator, use:
```
$ xcdo --show <operator>
```
<!--termynal--->
```
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


As it mimics the CDO interface, using XCDO is generally the same as using CDO. for e.g:
<!--termynal--->
```
$ xcdo -selvar,var1 indata.nc outdata.nc
$ xcdo -timemean -zonmean in.nc out.nc
```

## Custom Operators
A simple python function can be used as a custom operator of XCDO.
For example: a simple operator to print the dataset to terminal can be defined as follows in file a `dump.py`:

```python
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

Notice the ".py" extension for the custom operator? Yes, basically the operator name is just the path of the python file.

You can see the signature and documentation of the custom operator by running:

```bash
$ xcdo --show dump.py

╭─ Synopsis ──────────────────────────────────────────────────╮
│                                                             │
│  xcdo -dump.py input                                        │
│                                                             │
╰─────────────────────────────────────────────────────────────╯

```

<!--For a more complete example including more features, see the Tutorial - User Guide.-->
