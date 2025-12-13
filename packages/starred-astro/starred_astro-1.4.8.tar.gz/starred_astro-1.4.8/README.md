# STARRED: STARlet REgularized Deconvolution 

[![pipeline status](https://gitlab.com/cosmograil/starred/badges/main/pipeline.svg)](https://gitlab.com/cosmograil/starred/commits/main)
[![coverage report](https://gitlab.com/cosmograil/starred/badges/main/coverage.svg)](https://cosmograil.gitlab.io/starred/coverage/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-31114/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![DOI](https://joss.theoj.org/papers/10.21105/joss.05340/status.svg)](https://doi.org/10.21105/joss.05340)
[![pypi](https://img.shields.io/pypi/v/starred-astro.svg)](https://pypi.org/project/starred-astro/)

STARlet REgularized Deconvolution (STARRED) is a Python deconvolution method powered by Starlet regularization and JAX automatic differentiation. It uses a Point Spread Function (PSF) narrower than the original one as kernel.

The main Documentation can be found [here](https://cosmograil.gitlab.io/starred/)

## Installation 

### Through PyPI

STARRED releases are distributed through the Python Package Index (PyPI). To install the latest version use `pip`:

```bash
$ pip install starred-astro
```

### Through Anaconda
We provide an Anaconda environment that satisfies all the dependencies in `starred-env.yml`. 
```bash
$ git clone https://gitlab.com/cosmograil/starred.git
$ cd starred
$ conda env create -f starred-env.yml
$ conda activate starred-env
$ pip install .
```
In case you have an NVIDIA GPU, this should automatically download the right version of JAX as well as cuDNN.
Next, you can run the tests to make sure your installation is working correctly.

```bash
# While still in the STARRED directory:
$ pytest . 
```

### Manually handling the dependencies
If you want to use an existing environment, just omit the Anaconda commands above:
```bash
$ git clone https://gitlab.com/cosmograil/starred
$ cd starred 
$ pip install .
```

or if you need to install it for your user only: 
```bash
$ python setup.py install --user 
```

STARRED runs much faster on GPUs, so make sure you install a version of JAX that is compatible 
with your version of CUDA and cuDNN. 
Refer to the [installation page](https://jax.readthedocs.io/en/latest/installation.html) of the JAX documentation.

## Requirements 

STARRED requires the following Python packages: 
* `astropy`
* `dill`
* `jax`
* `jaxlib`
* `jaxopt`
* `matplotlib`
* `numpy`
* `scipy`
* `optax`
* `tqdm`
* `h5py`

Additionnaly, the following package needs to be installed if you want to sample posterior distribution: 
* `emcee`
* `mclmc`

Other optional dependencies are required for specific functionalities:

* `scikit-image` for the reconstruction of the narrow PSF from a PSF model.
* `pyregion` for the reading of DS9 region files.

## Example Notebooks and Documentation

We provide several notebooks to help you get started.

> [Start here to grasp the basic STARRED workflow](https://gitlab.com/cosmograil/starred/-/blob/main/notebooks/start_here.ipynb).

More example notebooks going in more detail of how the internals work can be found in the [notebooks](https://gitlab.com/cosmograil/starred/-/tree/main/notebooks/more_examples) directory: 
* [Ground-based narrow PSF generation](https://gitlab.com/cosmograil/starred/-/blob/main/notebooks/more_examples/1_WFI%20narrow%20PSF%20generation.ipynb)
* [Ground-based joint deconvolution](https://gitlab.com/cosmograil/starred/-/blob/main/notebooks/more_examples/2_DESJ0602-4335%20joint%20deconvolution.ipynb)
* [Another ground-based joint deconvolution](https://gitlab.com/cosmograil/starred/-/blob/main/notebooks/more_examples/3_Another%20lensed%20quasar%20-%20joint%20deconvolution.ipynb)
* [JWST PSF generation and deconvolution](https://gitlab.com/cosmograil/starred/-/blob/main/notebooks/more_examples/4_JWST%20deconvolution.ipynb)
* [DES2038 joint deconvolution](https://gitlab.com/cosmograil/starred/-/blob/main/notebooks/more_examples/5_DES2038_from_WFI_joint_deconvolution.ipynb)
* [HST PSF reconstruction](https://gitlab.com/cosmograil/starred/-/blob/main/notebooks/more_examples/6_HST-PSF%20reconstruction.ipynb)
* [JWST PSF reconstruction](https://gitlab.com/cosmograil/starred/-/blob/main/notebooks/more_examples/7_JWST-PSF_reconstruction.ipynb)

The mathematical formalism along with further examples are also presented
in [Millon et al. (2024)](https://arxiv.org/abs/2402.08725). All the examples and tests presented in this paper can be
reproduced from this repository:

* [STARRED Examples](https://gitlab.com/cosmograil/starred-examples)

You can also run STARRED from the command line by following
these [instructions](https://gitlab.com/cosmograil/starred/-/tree/main/scripts?ref_type=heads). STARRED is now fully
integrated into [lightcurver](https://github.com/duxfrederic/lightcurver),  
which helps you producing light curves by preparing your data in the correct format to be analyzed by STARRED and ensure
accurate epoch-to-epoch photometric calibration.

Finally, the full documentation can be found [here](https://cosmograil.gitlab.io/starred/) and a video presentation of
STARRED is accessible on [Youtube](https://www.youtube.com/watch?v=04FKFMBpSlo).

## STARRED users community

If you want to join the STARRED users community on Slack to ask questions, propose future developments or share your
latest results,
please send an email to [this address](mailto:martin.millon@hotamil.fr) to get an invitation link.

## Attribution

If you use this code, please cite [Michalewicz et al. 2023](https://joss.theoj.org/papers/10.21105/joss.05340)
and [Millon et al. 2024](https://arxiv.org/abs/2402.08725)
as indicated in the [documentation](https://cosmograil.gitlab.io/starred/citing.html).

## License
STARRED is a free software. You can redistribute it and/or modify it under the terms of the 
GNU General Public License as published by the Free Software Foundation.

STARRED is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY, without 
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
General Public License for more details ([LICENSE.txt](LICENSE)).
