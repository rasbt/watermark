#!/usr/bin/env bash

set -e

if [ "${TRAVIS_PYTHON_VERSION}" == "2.7" ]; then
    wget https://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh;
else
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh;
fi

bash miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
hash -r
conda config --set always_yes yes --set changeps1 no
conda update -q conda
conda info -a

conda create -n testenv python=$TRAVIS_PYTHON_VERSION ipython;
source activate testenv;

python --version;
python -c 'import IPython';
python setup.py install;
