# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['debiased_spatial_whittle',
 'debiased_spatial_whittle.grids',
 'debiased_spatial_whittle.inference',
 'debiased_spatial_whittle.models',
 'debiased_spatial_whittle.sampling']

package_data = \
{'': ['*']}

install_requires = \
['autograd>=1.5,<2.0',
 'matplotlib>=3.7.0,<4.0.0',
 'numpy>=1.21.5,<2.0.0',
 'param>=2.1.1,<3.0.0',
 'progressbar2>=4.2.0,<5.0.0',
 'pytest-cov>=6.2.1,<7.0.0',
 'scipy>=1.7.3,<2.0.0',
 'seaborn>=0.12.2,<0.13.0']

extras_require = \
{'gpu11': ['cupy-cuda11x', 'torch==2.2.2'],
 'gpu12': ['cupy-cuda12x>=13.0.0,<14.0.0', 'torch==2.2.2']}

setup_kwargs = {
    'name': 'debiased-spatial-whittle',
    'version': '2.1.2',
    'description': 'Spatial Debiased Whittle likelihood for fast inference of spatio-temporal covariance models from gridded data',
    'long_description': '# Spatial Debiased Whittle Likelihood\n\n![Image](logo.png)\n\n[![Documentation Status](https://readthedocs.org/projects/debiased-spatial-whittle/badge/?version=latest)](https://debiased-spatial-whittle.readthedocs.io/en/latest/?badge=latest)\n[![.github/workflows/run_tests_on_push.yaml](https://github.com/arthurBarthe/debiased-spatial-whittle/actions/workflows/run_tests_on_push.yaml/badge.svg)](https://github.com/arthurBarthe/debiased-spatial-whittle/actions/workflows/run_tests_on_push.yaml)\n[![Pypi](https://github.com/arthurBarthe/debiased-spatial-whittle/actions/workflows/pypi.yml/badge.svg)](https://github.com/arthurBarthe/debiased-spatial-whittle/actions/workflows/pypi.yml)\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/arthurBarthe/debiased-spatial-whittle/master)\n\n## Introduction\n\nThis package implements the Spatial Debiased Whittle Likelihood (SDW) as presented in the article of the same name, by the following authors:\n\n- Arthur P. Guillaumin\n- Adam M. Sykulski\n- Sofia C. Olhede\n- Frederik J. Simons\n\nAdditionally, the following people have greatly contributed to further developments of the method and its implementation:\n- Thomas Goodwin\n- Olivia L. Walbert\n\nThe SDW extends ideas from the Whittle likelihood and Debiased Whittle Likelihood to random fields and spatio-temporal data. In particular, it directly addresses the bias issue of the Whittle likelihood for observation domains with dimension greater than 2. It also allows us to work with rectangular domains (i.e., rather than square), missing observations, and complex shapes of data.\n\nThe documentation is available [here](https://debiased-spatial-whittle.readthedocs.io/en/latest/?badge=latest).\n\n## Installation instructions\n\n### CPU-only\n\nThe package can be installed via one of the following methods.\n\n1. Via the use of [Poetry](https://python-poetry.org/), by running the following command:\n\n   ```bash\n   poetry add debiased-spatial-whittle\n   ```\n\n2. Otherwise, you can directly install via pip:\n\n    ```bash\n    pip install debiased-spatial-whittle\n    ```\n\n### GPU\nThe Debiased Spatial Whittle likelihood relies on the Fast Fourier Transform (FFT) for computational efficiency.\nGPU implementations of the FFT provide additional computational efficiency (order x100) at almost no additional cost thanks to GPU implementations of the FFT algorithm.\n\nIf you want to install with GPU dependencies (Cupy and Pytorch):\n\n1. You need an NVIDIA GPU\n2. You need to install the CUDA Toolkit. See for instance Cupy\'s [installation page](https://docs.cupy.dev/en/stable/install.html).\n3. You can install Cupy or pytorch yourself in your environment. Or you can specify an extra to poetry, e.g.\n\n   ```bash\n   poetry add debiased-spatial-whittle -E gpu12\n   ```\n   if you version of the CUDA toolkit is 12.* (use gpu11 if your version is 11.*)\n\nOne way to check your CUDA version is to run the following command in a terminal:\n\n```bash\n   nvidia-smi\n```\n\nYou can then switch to using e.g. Cupy instead of numpy as the backend via:\n\n   ```python\n    from debiased_spatial_whittle.backend import BackendManager\n    BackendManager.set_backend("cupy")\n   ```\n\nThis should be run before any other import from the debiased_spatial_whittle package.\n\n\n## PyPI\nThe package is updated on PyPi automatically on creation of a new\nrelease in Github. Note that currently the version in pyproject.toml\nneeds to be manually updated. This should be fixed by adding\na step in the workflow used for publication to Pypi.\n',
    'author': 'arthur',
    'author_email': 'ahw795@qmul.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://arthurpgb.pythonanywhere.com/sdw',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
