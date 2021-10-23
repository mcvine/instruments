#!/usr/bin/env python
# coding: utf-8

# # Convert detector systems from mantid xml to mcvine
# 

import os, sys, shutil
import mantid
from mantid import simpleapi

# some goodies
import numpy as np, histogram.hdf as hh, histogram as H


# ## Create workflow
workdir = os.path.expanduser('~/simulations/AMATERAS/detsys')
if not os.path.exists(workdir):
    os.makedirs(workdir)

#!rm -rf {workdir}/*
os.chdir(workdir)

# ## Convert
import mantid2mcvine as m2m
shutil.copyfile(
    '/home/97n/dv/mcvine/instruments/AMATERAS/detector_system/AMATERAS_detector_2021_tubegap.xml',
    'AMATERAS_Definition_06162021.xml')

mantid_idf = "AMATERAS_Definition_06162021.xml"
# output
mcvine_idf = 'AMATERAS_mcvine_06162021.xml'
template_nxs = 'amateras_template_06162021.nxs'
tofbinsize = 0.1 # mus

detsys_shape = m2m.shapes.hollowCylinder(in_radius=4., out_radius=5., height=9.) # meters
im = m2m.InstrumentModel(
    instrument_name='AMATERAS', beamline=2099,
    mantid_idf=mantid_idf, mcvine_idf=mcvine_idf, template_nxs=template_nxs,
    detsys_shape=detsys_shape,  mantid_idf_monitor_tag = 'monitors',
    tofbinsize = tofbinsize,
    )
im.convert()

import yaml
with open('amateras_instrument_model_06162021.yaml', 'wt') as stream:
    yaml.safe_dump(im.todict(), stream)
