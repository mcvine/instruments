# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

import numpy as np

def populate_Ei_data(sim_out, nxs):
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


# this is almost the same as the ARCS version
# this is different from the previous sequoia-reduce-nxs-using-mantid
# since the nxspe write out is not implemented here.
# NXSPE may not be necessary because we can just use the code
# in mcvine workflow single crystal reduce scripts and skip nxspe
def reduce(nxsfile, qaxis, outfile, use_ei_guess=False, ei_guess=None, eaxis=None, tof2E=True, ibnorm='ByCurrent'):
    from mantid.simpleapi import DgsReduction, SofQW3, SaveNexus, LoadInstrument, Load, MoveInstrumentComponent, \
        MaskBTP, ConvertToMD, BinMD, ConvertMDHistoToMatrixWorkspace, GetEiT0atSNS, GetEi
    from mantid import mtd
    ws = Load(nxsfile)
    
    if tof2E == 'guess':
        axis = ws.getAxis(0).getUnit().caption().lower()
        # axis name should be "Time-of-flight"
        tof2E = "time" in axis and "flight" in axis
    
    if tof2E:
        # mask packs around beam
        # MaskBTP(ws, Bank="98-102")
        if not use_ei_guess:
            run = ws.getRun()
            Efixed = run.getLogData('mcvine-Ei').value
            T0 = run.getLogData('mcvine-t0').value
        else:
            Efixed, T0 = ei_guess, 0

        DgsReduction(
            SampleInputWorkspace=ws,
            IncidentEnergyGuess=Efixed,
            UseIncidentEnergyGuess=True,
            TimeZeroGuess = T0,
            OutputWorkspace='reduced',
            EnergyTransferRange=eaxis,
            IncidentBeamNormalisation=ibnorm,
            )
        reduced = mtd['reduced']
    else: 
        reduced = Load(nxsfile)

    # if eaxis is not specified, use the data in reduced workspace
    if eaxis is None:
        Edim = reduced.getXDimension()
        emin = Edim.getMinimum()
        emax = Edim.getMaximum()
        de = Edim.getX(1) - Edim.getX(0)
        eaxis = emin, de, emax
        
    qmin, dq, qmax = qaxis; nq = int(round((qmax-qmin)/dq))
    emin, de, emax = eaxis; ne = int(round((emax-emin)/de))
    md = ConvertToMD(
        InputWorkspace='reduced',
        QDimensions='|Q|',
        dEAnalysisMode='Direct',
        MinValues="%s,%s" % (qmin, emin),
        MaxValues="%s,%s" % (qmax, emax),
        SplitInto="%s,%s" % (nq, ne),
        )
    binned = BinMD(
        InputWorkspace=md,
        AxisAligned=1,
        AlignedDim0="|Q|,%s,%s,%s" % (qmin, qmax, nq),
        AlignedDim1="DeltaE,%s,%s,%s" % (emin, emax, ne),
        )
    # convert to histogram
    import histogram as H, histogram.hdf as hh
    data=binned.getSignalArray().copy()
    err2=binned.getErrorSquaredArray().copy()
    nev=binned.getNumEventsArray()
    data/=nev
    err2/=(nev*nev)
    qaxis = H.axis('Q', boundaries=np.arange(qmin, qmax+dq/2., dq), unit='1./angstrom')
    eaxis = H.axis('E', boundaries=np.arange(emin, emax+de/2., de), unit='meV')
    hist = H.histogram('IQE', (qaxis, eaxis), data=data, errors=err2)
    if outfile.endswith('.nxs'):
        import warnings
        warnings.warn("reduce function no longer writes iqe.nxs nexus file. it only writes iqe.h5 histogram file")
        outfile = outfile[:-4] + '.h5'
    hh.dump(hist, outfile)
    return


# do we still need MoveInstrumentComponent?
"""
    # load workspace from input nexus file
    workspace = Load(nxsfile)
    
    # XXX: the following line seems to cause trouble. probably a bug in Mantid?
    # LoadInstrument(workspace, idfpath) 
    
    # change moderator position
    # mantid: z=-20.0114
    # mcvine: z=-20.0254
    # need shift: z=-0.014
    MoveInstrumentComponent(workspace, "moderator", -1, 0, 0, -0.014, True) # workspace, component, detector, x,y,z, relative
    # MoveInstrumentComponent(workspace, "moderator", -1, 0, 0, -20.0254, False) # workspace, component, detector, x,y,z, relative

"""
