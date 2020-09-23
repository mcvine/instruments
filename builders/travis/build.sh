#!/bin/bash

conda config --set always_yes true
conda update conda
conda config --add channels conda-forge
conda config --add channels diffpy
conda config --add channels mantid
conda config --add channels mcvine

conda create -n testenv python=$TRAVIS_PYTHON_VERSION
source activate testenv
conda install -c mcvine/label/unstable mcvine-core=1.3.5 mantid-framework=4.0.0 mantid2mcvine
export SRC=$PWD
export PYVER=${TRAVIS_PYTHON_VERSION}
export PREFIX=${CONDA_PREFIX}
echo $PYVER
echo $PREFIX
PY_INCLUDE_DIR=${PREFIX}/include/`ls ${PREFIX}/include/|grep python${PYVER}`
PY_SHAREDLIB=${PREFIX}/lib/`ls ${PREFIX}/lib/|grep libpython${PYVER}[a-z]*.so$`
echo $PY_INCLUDE_DIR
echo $PY_SHAREDLIB
export BLD_ROOT=$SRC/build
mkdir -p $BLD_ROOT && cd $BLD_ROOT
cmake $SRC -DCMAKE_INSTALL_PREFIX=$PREFIX -DPYTHON_LIBRARY=$PY_SHAREDLIB -DPYTHON_INCLUDE_DIR=$PY_INCLUDE_DIR
  #  -DDEPLOYMENT_PREFIX=/home/lj7/miniconda2/envs/dev-mcvine -DCMAKE_SYSTEM_LIBRARY_PATH=/home/lj7/miniconda2/envs/dev-mcvine/lib 
make install

