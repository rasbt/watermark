#!/usr/bin/env bash

python --version
python setup.py install;
python -c "import watermark; print('watermark %s' % watermark.__version__)";
