#!/usr/bin/env python
# -*- coding: utf-8 -*-

# +---------------------------------------------------------------------------+
# |  cue - Lightweight GPU Job Scheduler                                      |
# |                                                                           |
# |  A streamlined workload manager designed for Deep Learning research,      |
# |  optimizing GPU usage for individuals and small teams.                    |
# |                                                                           |
# |  Repository: https://github.com/Sureshmohan19/cue-ml                      |
# +---------------------------------------------------------------------------+

import os
import sys
from shutil import rmtree
from setuptools import find_packages, setup, Command

# Configuration
PACKAGE_NAME = 'cuepy' 
REQUIRES_PYTHON = '>=3.10.0'

# Python Version Check
CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON_TUPLE = (3, 10)

if CURRENT_PYTHON < REQUIRED_PYTHON_TUPLE:
    sys.stderr.write("""

==========================
Unsupported Python version
==========================
This package requires at least Python {}.{}.
You are currently using Python {}.{}.
""".format(*(REQUIRED_PYTHON_TUPLE + CURRENT_PYTHON)))
    sys.exit(1)

# Load Metadata
here = os.path.abspath(os.path.dirname(__file__))
about = {}

# This reads cuepy/__version__.py
version_path = os.path.join(here, PACKAGE_NAME, "__version__.py")
with open(version_path, "r", encoding="utf-8") as f:
    exec(f.read(), about)

# Import the README and use it as the long-description.
try:
    with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = about['__description__']

# Upload Support
class UploadCommand(Command):
    """Support setup.py publish."""
    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self): pass
    def finalize_options(self): pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel…')
        os.system('{0} setup.py sdist bdist_wheel'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')
        sys.exit()

# Setup
setup(
    # This comes from __version__.py
    name=about['__title__'], 
    version=about['__version__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=about['__url__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    license=about['__license__'],
    
    python_requires=REQUIRES_PYTHON,
    
    # Auto-finds 'cuepy'
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    
    install_requires=[
        "PyYAML>=6.0",
    ],

    extras_require={
        'test': [
            'pytest>=7.0',
            'pytest-cov',
        ],
        'dev': [
            'black',
            'isort',
            'twine',
            'wheel',
        ],
    },
    
    entry_points={
        'console_scripts': [
            f'cue={PACKAGE_NAME}.__main__:main', 
        ],
    },
    
    cmdclass={
        'upload': UploadCommand,
    },
    
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: System :: Distributed Computing',
    ],
)