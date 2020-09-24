# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

import sys

def populate_metadata(sim_out, nxs, sample, detector):
    if sys.version_info<(3,0) and isinstance(nxs, unicode):
        nxs = nxs.encode('utf-8')
    import h5py
    f = h5py.File(nxs, 'a')
    entry = f['entry']
    from mcvine.instruments.HYSPEC.nxs.raw import populateMetadata
    populateMetadata(entry, sim_out, sample, detector)
    f.close()
    # add log entries
    import ast, os
    props = ast.literal_eval(open(os.path.join(sim_out, 'props.json')).read())
    Ei, unit = props['average energy'].split(); assert unit=='meV'
    t0, unit = props['emission time'].split(); assert unit=='microsecond'
    from mantid import simpleapi as msa
    ws = msa.Load(nxs)
    msa.AddSampleLog(ws, LogName='mcvine-Ei', LogText=str(Ei), LogType='Number')
    msa.AddSampleLog(ws, LogName='mcvine-t0', LogText=str(t0), LogType='Number')
    msa.SaveNexus(ws, nxs)
    return

# End of file
