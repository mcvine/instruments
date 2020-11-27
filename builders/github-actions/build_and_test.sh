#!/bin/bash

set -e
set -x

export SRC=$PWD
export PREFIX=$CONDA_PREFIX

PY_INCLUDE_DIR=${PREFIX}/include/`ls ${PREFIX}/include/|grep python${PYTHON_VERSION}`
PY_SHAREDLIB=${PREFIX}/lib/`ls ${PREFIX}/lib/|grep libpython${PYTHON_VERSION}[a-z]*.so$`
echo $PY_INCLUDE_DIR
echo $PY_SHAREDLIB

export BLD_ROOT=$SRC/build
mkdir -p $BLD_ROOT && cd $BLD_ROOT 
cmake \
    -DCMAKE_INSTALL_PREFIX=$PREFIX \
    -DPYTHON_LIBRARY=$PY_SHAREDLIB \
    -DPYTHON_INCLUDE_DIR=$PY_INCLUDE_DIR \
    $SRC
make install

CTEST_OUTPUT_ON_FAILURE=1 make test
