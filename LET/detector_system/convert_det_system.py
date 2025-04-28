#!/usr/bin/env python
# coding: utf-8

# Convert detector systems from mantid xml to mcvine
#

import os, sys, shutil
import mantid
import numpy as np

# ## Create workflow
workdir = os.path.expanduser('~/simulations/LET/detsys')
if not os.path.exists(workdir):
    os.makedirs(workdir)

#!rm -rf {workdir}/*
os.chdir(workdir)

# ## Convert
import mantid2mcvine as m2m
shutil.copyfile(
    '/home/97n/dv/mcvine/instruments/LET/detector_system/LET_detector_2021.xml',
    'LET_Definition_10232021.xml')

mantid_idf = "LET_Definition_10232021.xml"
# output
mcvine_idf = 'LET_mcvine_10232021.xml'
template_nxs = 'LET_template_10232021.nxs'
tofbinsize = 0.1 # mus

detsys_shape = m2m.shapes.hollowCylinder(in_radius=3., out_radius=4., height=5.) # meters
im = m2m.InstrumentModel(
    instrument_name='LET', beamline=2199,
    mantid_idf=mantid_idf, mcvine_idf=mcvine_idf, template_nxs=template_nxs,
    detsys_shape=detsys_shape,  mantid_idf_monitor_tag = 'monitors',
    tofbinsize = tofbinsize,
    )
im.convert()

import yaml
with open('LET_instrument_model_10232021.yaml', 'wt') as stream:
    yaml.safe_dump(im.todict(), stream)
