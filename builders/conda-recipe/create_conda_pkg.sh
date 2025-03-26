#!/bin/bash

# prerequisites
# 1. in test conda environment
# 2. in conda-recipe directory with meta.yaml.template
# 3. defined env vars:
#    - PYTHON_VERSION
#    - _CONDA_PKG_NAME_
#    - _CONDA_PKG_ARCH_
#    - _CONDA_PKG_VER_
#    - _GIT_REV_
#    - CONDA_UPLOAD_TOKEN

set -e
set -x

conda config --show channels
conda install -n root conda-build
conda install anaconda-client
which conda
which anaconda
conda config --set anaconda_upload no

# build
cd $(realpath $(dirname $0))
pwd
sed -e "s|XXXVERSIONXXX|$_CONDA_PKG_VER_|g" meta.yaml.template | sed -e "s|XXXGIT_REVXXX|$_GIT_REV_|g" > meta.yaml
cat meta.yaml
conda build --python=$PYTHON_VERSION .

# upload
CONDA_ROOT_PREFIX=$(realpath $(dirname `which conda`)/..)
anaconda -t $CONDA_UPLOAD_TOKEN upload --force --label unstable \
         $CONDA_ROOT_PREFIX/conda-bld/$_CONDA_PKG_ARCH_/$_CONDA_PKG_NAME_-$_CONDA_PKG_VER_-*.conda
