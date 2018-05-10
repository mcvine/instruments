#!/usr/bin/env python
#
#   Jiao Lin
#

def populate_Ei_data(sim_out, nxs):
    import ast, os
    props = ast.literal_eval(open(os.path.join(sim_out, 'props.json')).read())
    Ei, unit = props['average energy'].split(); assert unit=='meV'
    t0, unit = props['emission time'].split(); assert unit=='microsecond'
    setEnergyRequest(nxs, float(Ei))
    from mantid import simpleapi as msa
    if isinstance(nxs, unicode):
        nxs = nxs.encode('utf-8')
    ws = msa.Load(nxs)
    msa.AddSampleLog(ws, LogName='mcvine-Ei', LogText=str(Ei), LogType='Number')
    msa.AddSampleLog(ws, LogName='mcvine-t0', LogText=str(t0), LogType='Number')
    msa.SaveNexus(ws, nxs)
    return


def setEnergyRequest(path, Ei):
    """set energy request value into an CNCS processed nexus file
    
    path: path of the nexus file
    Ei: unit meV
    
    caveat: the nexus template file should already have /???workspace???/logs/EnergyRequest which contains the appropriate sub-datasets with correct attributes.
    """
    import h5py
    f = h5py.File(path, 'a')
    # XXX assume the workspace is the first node at root XXX
    ws = f.values()[0]
    logs = ws['logs']
    er = logs['EnergyRequest']
    er['value'][0] = Ei
    f.close()
    return


def reduce(nxsfile, qaxis, outfile, use_ei_guess=False, ei_guess=None, eaxis=None, tof2E=True, ibnorm='ByCurrent', t0_guess=None):
    from ...ARCS.applications.nxs import reduce
    reduce(
        nxsfile, qaxis, outfile,
        use_ei_guess=use_ei_guess, ei_guess=ei_guess,
        eaxis=eaxis, tof2E=tof2E, ibnorm=ibnorm,
        t0_guess=t0_guess, use_monitors=False)


# End of file 
