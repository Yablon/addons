# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""TensorFlow Addons.

TensorFlow Addons is a repository of contributions that conform to well-
established API patterns, but implement new functionality not available
in core TensorFlow. TensorFlow natively supports a large number of
operators, layers, metrics, losses, and optimizers. However, in a fast
moving field like ML, there are many interesting new developments that
cannot be integrated into core TensorFlow (because their broad
applicability is not yet clear, or it is mostly used by a smaller subset
of the community).
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import platform
import sys

from datetime import datetime
from setuptools import find_packages
from setuptools import setup
from setuptools.dist import Distribution
from setuptools import Extension

DOCLINES = __doc__.split('\n')

TFA_NIGHTLY = 'tfa-nightly'
TFA_RELEASE = 'tensorflow-addons'

if '--nightly' in sys.argv:
    project_name = TFA_NIGHTLY
    nightly_idx = sys.argv.index('--nightly')
    sys.argv.pop(nightly_idx)
else:
    project_name = TFA_RELEASE

# Version
version = {}
base_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base_dir, "tensorflow_addons", "version.py")) as fp:
    # yapf: disable
    exec(fp.read(), version)
    # yapf: enable

if project_name == TFA_NIGHTLY:
    version['__version__'] += datetime.strftime(datetime.today(), "%Y%m%d")

# Dependencies
REQUIRED_PACKAGES = [
    'six >= 1.10.0',
]

if project_name == TFA_RELEASE:
    # TODO: remove if-else condition when tf supports package consolidation.
    if platform.system() == 'Linux':
        REQUIRED_PACKAGES.append('tensorflow-gpu == 2.0.0')
    else:
        REQUIRED_PACKAGES.append('tensorflow == 2.0.0')
elif project_name == TFA_NIGHTLY:
    REQUIRED_PACKAGES.append('tf-nightly')


class BinaryDistribution(Distribution):
    """This class is needed in order to create OS specific wheels."""

    def has_ext_modules(self):
        return True


setup(
    name=project_name,
    version=version['__version__'],
    description=DOCLINES[0],
    long_description='\n'.join(DOCLINES[2:]),
    author='Google Inc.',
    author_email='opensource@google.com',
    packages=find_packages(),
    ext_modules=[Extension('_foo', ['stub.cc'])],
    install_requires=REQUIRED_PACKAGES,
    include_package_data=True,
    zip_safe=False,
    distclass=BinaryDistribution,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
    ],
    license='Apache 2.0',
    keywords='tensorflow addons machine learning',
)
