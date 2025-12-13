# Adding the STARRED package to sys path so submodules can be called directly

import inspect
import os
import sys

__all__ = ["deconvolution", "plots", "psf", "utils"]

# Needed only if there is no path pointing to the root directory. Mostly for testing purposes.
path_ = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
sys.path.append(path_)
