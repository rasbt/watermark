# Sebastian Raschka 2014-2025
# IPython magic function to print date/time stamps and
# various system information.
# Author: Sebastian Raschka <sebastianraschka.com>
#
# License: BSD 3 clause

from os.path import dirname, join, realpath
from setuptools import find_packages, setup


PROJECT_ROOT = dirname(realpath(__file__))
REQUIREMENTS_FILE = join(PROJECT_ROOT, "requirements.txt")
README_FILE = join(PROJECT_ROOT, "README.md")

with open(REQUIREMENTS_FILE, encoding="utf-8") as f:
    install_reqs = f.read().splitlines()

install_reqs.append("setuptools")

with open(README_FILE, encoding="utf-8") as f:
    long_description = f.read()

# Also see settings in setup.cfg
setup(
    name="watermark",
    license="newBSD",
    description=(
        "IPython magic function to print date/time stamps and "
        "various system information."
    ),
    author="Sebastian Raschka",
    author_email="mail@sebastianraschka.com",
    url="https://github.com/rasbt/watermark",
    packages=find_packages(exclude=[]),
    install_requires=install_reqs,
    extras_require={'gpu': ['py3nvml>=0.2']},
    long_description=long_description,
    long_description_content_type="text/markdown",
)
