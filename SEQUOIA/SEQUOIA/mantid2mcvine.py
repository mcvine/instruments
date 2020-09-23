#!/usr/bin/env python

# This script is to be called by the installation script
# python <this-script> <target_dir>
# target_dir is usually $PREFIX/instrument

from __future__ import absolute_import
import os, sys, yaml
from . import mantid2mcvine as m2m
here = os.path.dirname(__file__)

def loadInstrumentModel():
    d = yaml.load(open(os.path.join(here, "SEQ_virtual.yml")))
    # update paths
    d.update(
        mcvine_idf=os.path.join(here, 'SEQ_virtual_12292017_mcvine.xml'),
        template_nxs=os.path.join(here, 'SEQ_virtual_template_12292017.nxs')
    )
    return m2m.InstrumentModel(**d)

def install_mantid_IDF():
    fn = 'SEQ_virtual_Definition_12292017.xml'
    if os.path.exists(os.path.expanduser('~/.mantid/instrument/%s' % fn)): return
    im = loadInstrumentModel()
    im.mantid_idf = os.path.join(here, fn)
    im.mantid_install()
    return

install_mantid_IDF()
