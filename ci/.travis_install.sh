#!/usr/bin/env bash

set -e

wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh;
bash miniconda.sh -b -p $HOME/miniconda
source "$HOME/miniconda/etc/profile.d/conda.sh"
hash -r
conda config --set always_yes yes --set changeps1 no
conda update -q conda
conda info -a

conda create -n testenv python=$PYTHON_VERSION -c conda-forge;
conda activate testenv;

python --version;

if [[ "$PYTHON_VERSION" == "2.7" ]]; then
  python -m pip install ipython;
  python -m pip install . --ignore-requires-python;
else
  python -m pip install .;
fi
