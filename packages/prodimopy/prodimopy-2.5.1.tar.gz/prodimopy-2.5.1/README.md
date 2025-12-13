# prodimopy

Python package for

- reading and plotting ProDiMo results
- running, reading, plotting 0D slab models
- chi2 fitting of observed spectra with slab models

Any bug reports or feature requests are very welcome (You can do that [here](https://gitlab.astro.rug.nl/prodimo/prodimopy/-/issues?sort=created_date&state=opened)).
If you want to contribute some code please contact me (Christian Rab).

[[_TOC_]]

## Documentation

Please check out the documentation! Click on the badge! There you will also find several code examples on how to use the package.

[![Documentation Status](https://readthedocs.org/projects/prodimopy/badge/?version=latest)](https://prodimopy.readthedocs.io/en/latest/?badge=latest)

## Requirements

prodimopy uses several additional python packages which are commonly used in the astronomical community.

The following packages are required

| Package           | Version     | Comment                            |
|-------------------|-------------|------------------------------------|
| _astropy_         | >= 5.1      |                                    |
| _numpy_           | >= 1.20     |                                    |
| _scipy_           | >= 1.7.1    |                                    |
| _f90nml_          | >= 1.4.4    |                                    |
| _matplotlib_      | >= 3.7      | only required for plotting         |
| _pandas_          | >= 1.5.1    | only required for slab models      |
| _adjustText_      | >= 0.8      | only required for slab models      |
| _spectres_        | >= 2.2.0    | only required for slab models      |
| _dust_extinction_ | >= 1.5      | only required for reddening SEDs.  |

If you use the setup script (see Installation) those packages will be installed automatically if necessary. **We only support python3**, and highly recommend a python version >=3.9.

## Installation

Installation via source (most recent version from gitlab repository) and pip (latest stable version) is supported.

If you use prodimopy in combination with the ProDiMo code and work with the master branch there we recommmend to 
use the installation from source, to make sure you have the most recent version of prodimopy as well. Source installation
is also recommended if you want to contribute to the code (you are very welcome to do so).

In all other cases a simple pip install is recommended.

### via pip (for Users)

If you just want a stable version use pip to install the project. Just type in the command line

```console
pip install prodimopy
```

to upgrade to a new version you can also use pip. We recommend to do it this way.

```console
pip install --upgrade --upgrade-strategy only-if-needed prodimopy
```

### from source (for Developers)

If you always want to have the most recent version clone this repository and install the package directly from the source:

- change into a directory of your choice and
- clone the repository (git will create a new directory called prodimopy)

  ```console
  git clone https://gitlab.astro.rug.nl/prodimo/prodimopy.git
  ```

- change into the newly created prodimopy directory and type (**don't use** `--user` if you are using a dedicated conda environment for prodimopy):

  ```console
  pip install --user -e .
  ```

  This will install the package in your current python environment (should be the one you want to use for ProDiMo). The `-e` options allows to update the python code (e.g. via git) without the need to reinstall the package. If you are using VS code and e.g. the Pylance extension, you might get a warning that the prodimopy imports cannot be resolved (for details see [Editable Installs](https://setuptools.pypa.io/en/latest/userguide/development_mode.html#development-mode-a-k-a-editable-installs)). The following command for the pip installation should fix this issue:

  ```console
  pip install -e . --config-settings editable_mode=strict
  ```

To update the code simply type

  ```console
  git pull 
  ```

in the prodimopy directory. You can directly use the updated code and usually no reinstall of the package is required. However, if you run into problems you can try to reinstall the package with the pip command again.
