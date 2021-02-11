#!/bin/bash

export _GIT_REV_=`git describe --tags`
VERSION=`git describe --tags | cut -d '-' -f1 | cut -c2-`
VERSION_NEXT=`echo ${VERSION}| awk -F. -v OFS=. 'NF==1{print ++$NF}; NF>1{if(length($NF+1)>length($NF))$(NF-1)++; $NF=sprintf("%0*d", length($NF), ($NF+1)%(10^length($NF))); print}'`
echo ${VERSION} ${VERSION_NEXT}
export _CONDA_PKG_VER_=${VERSION_NEXT}.dev
export _CONDA_PKG_ARCH_=noarch
export _CONDA_PKG_NAME_=mcvine.instruments
echo building ${_CONDA_PKG_ARCH_} conda pkg ${_CONDA_PKG_NAME_} version:${_CONDA_PKG_VER_}    git version:${_GIT_REV_}
./builders/conda-recipe/create_conda_pkg.sh
