#!/usr/bin/env bash

source activate testenv;

set -e

python -c "import IPython; print('IPython %s' % IPython.__version__)";
python -c "import watermark; print('watermark %s' % watermark.__version__)";
ipython -c "%load_ext watermark";
