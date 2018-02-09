#!/usr/bin/env python

import os
import mantid2mcvine as m2m

instrument_name = 'SEQ_virtual'
beamline = 777001700012292017   # 777: prefix, 17: SEQ beamline number in mantid Facilities.xml, 12292017: date
mantid_idf = os.path.abspath('SEQ_virtual_Definition_12292017.xml')
mcvine_idf = os.path.abspath('SEQ_virtual_12292017_mcvine.xml')
template_nxs = os.path.abspath('SEQ_virtual_template_12292017.nxs')

detsys_shape = m2m.shapes.hollowCylinder(in_radius=4., out_radius=8., height=4.) # meters
nbanks = 113
ntubesperpack = 8
npixelspertube = 128

tube_info = m2m.TubeInfo(
        pressure = 10.*m2m.units.pressure.atm,
        radius = .5 * m2m.units.length.inch,
        gap = 0.02 * m2m.units.length.inch,
    )

tofbinsize = 0.1 # mus

im = m2m.InstrumentModel(
    instrument_name, beamline, mantid_idf, mcvine_idf, template_nxs,
    detsys_shape, tube_info,
    nbanks = nbanks,
    ntubesperpack = ntubesperpack,
    npixelspertube = npixelspertube,
    tofbinsize = tofbinsize,
    mantid_idf_row_typename_postfix = 'row'
)

im.convert()
d = im.todict()
import yaml
with open('%s.yml' % instrument_name, 'w') as ostream:
    yaml.dump(d, ostream, default_flow_style=False)
