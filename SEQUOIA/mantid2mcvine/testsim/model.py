import os
import mantid2mcvine as m2m

instrument_name = 'SEQ_virtual'
beamline = 777001700012292017   # 777: prefix, 17: SEQ beamline number in mantid Facilities.xml, 12292017: date
mantid_idf = None
mcvine_idf = os.path.abspath('../SEQ_virtual_12292017_mcvine.xml')
template_nxs = os.path.abspath('../SEQ_virtual_template_12292017.nxs')

detsys_shape = None
nbanks = 113
ntubesperpack = 8
npixelspertube = 128
nmonitors = 0
tube_info = None
tofbinsize = 0.1 # mus

im = m2m.InstrumentModel(
    instrument_name, beamline, mantid_idf, mcvine_idf, template_nxs,
    detsys_shape, tube_info,
    nbanks = nbanks,
    ntubesperpack = ntubesperpack,
    npixelspertube = npixelspertube,
    nmonitors = nmonitors,
    tofbinsize = tofbinsize,
    mantid_idf_row_typename_postfix = 'row'
)
