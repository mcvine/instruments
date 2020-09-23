# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

import sys

def nxsfilename_with_monitors(nxs):
    import os
    fn, ext = os.path.splitext(os.path.basename(nxs))
    return os.path.join(os.path.dirname(nxs), '%s-with-monitors.nxs' % fn)


def populate_Ei_data(sim_out, nxs):
    import shutil, os
    nxs_withmons = nxsfilename_with_monitors(nxs)
    shutil.copyfile(nxs, nxs_withmons)
    populate_monitor_data(sim_out, nxs_withmons)
    print((" * Created ARCS NeXus file with monitor data: %s" % nxs_withmons))
    #
    import ast
    props = ast.literal_eval(open(os.path.join(sim_out, 'props.json')).read())
    Ei, unit = props['average energy'].split(); assert unit=='meV'
    t0, unit = props['emission time'].split(); assert unit=='microsecond'
    from mantid import simpleapi as msa
    if sys.version_info < (3,0) and isinstance(nxs, unicode):
        nxs = nxs.encode('utf-8')
    ws = msa.Load(nxs)
    msa.AddSampleLog(ws, LogName='mcvine-Ei', LogText=str(Ei), LogType='Number')
    msa.AddSampleLog(ws, LogName='mcvine-t0', LogText=str(t0), LogType='Number')
    msa.SaveNexus(ws, nxs)
    return


def populate_monitor_data(sim_out, nxs):
    import h5py
    f = h5py.File(nxs, 'a')
    entry = f['entry']
    from mcvine.instruments.ARCS.nxs.raw import populateMonitors, populateEiData
    populateMonitors(entry, sim_out)
    populateEiData(entry, sim_out)
    f.close()
    return


def reduce(nxsfile, qaxis, outfile, use_ei_guess=False, ei_guess=None, eaxis=None, tof2E=True, ibnorm='ByCurrent', t0_guess=None, use_monitors=False):
    from mantid.simpleapi import DgsReduction, LoadInstrument, Load, MoveInstrumentComponent, GetEiT0atSNS, GetEi
    from mantid import mtd
    if sys.version_info < (3,0) and isinstance(nxs, unicode):
        nxsfile = nxsfile.encode('utf-8')

    if tof2E == 'guess':
        # XXX: this is a simple guess. all raw data files seem to have root "entry"
        cmd = 'h5ls %s' % nxsfile
        import subprocess as sp, shlex
        o = sp.check_output(shlex.split(cmd)).strip().split()[0]
        tof2E = o == 'entry'

    if tof2E:
        if not use_ei_guess and use_monitors:
            # use monitors
            ws, mons = Load(nxsfile, LoadMonitors=True)
            Eguess=ws.getRun()['EnergyRequest'].getStatistics().mean
            try:
                Efixed,_p,_i,T0=GetEi(InputWorkspace=mons,Monitor1Spec=1,Monitor2Spec=2,EnergyEstimate=Eguess,FixEi=False)
            except:
                import warnings
                warnings.warn("Failed to determine Ei from monitors. Use EnergyRequest log %s" % Eguess)
                Efixed,T0 = Eguess, 0
        else:
            ws = Load(nxsfile)
            if not use_ei_guess:
                # use Ei T0 saved from beam simulation
                run = ws.getRun()
                Efixed = run.getLogData('mcvine-Ei').value
                T0 = run.getLogData('mcvine-t0').value
            else:
                # use Ei guess from function parameters
                Efixed, T0 = ei_guess, t0_guess or 0.
        # van = SolidAngle(ws) # for solid angle normalization
        DgsReduction(
            SampleInputWorkspace=ws,
            IncidentEnergyGuess=Efixed,
            UseIncidentEnergyGuess=True,
            TimeZeroGuess = T0,
            OutputWorkspace='reduced',
            EnergyTransferRange=eaxis,
            IncidentBeamNormalisation=ibnorm,
            # DetectorVanadiumInputWorkspace=van,
            # UseProcessedDetVan=True
            )
        reduced = mtd['reduced']
    else: 
        reduced = Load(nxsfile)

    getSqeHistogramFromMantidWS(reduced, outfile, qaxis, eaxis)
    return


def getSqeHistogramFromMantidWS(reduced, outfile, qaxis=None, eaxis=None):
    from mantid import simpleapi as msa
    # if eaxis is not specified, use the data in reduced workspace
    if eaxis is None:
        Edim = reduced.getXDimension()
        emin = Edim.getMinimum()
        emax = Edim.getMaximum()
        de = Edim.getX(1) - Edim.getX(0)
        eaxis = emin, de, emax
        
    qmin, dq, qmax = qaxis; nq = int(round((qmax-qmin)/dq))
    emin, de, emax = eaxis; ne = int(round((emax-emin)/de))
    md = msa.ConvertToMD(
        InputWorkspace=reduced,
        QDimensions='|Q|',
        dEAnalysisMode='Direct',
        MinValues="%s,%s" % (qmin, emin),
        MaxValues="%s,%s" % (qmax, emax),
        )
    binned = msa.BinMD(
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
    import numpy as np
    qaxis = H.axis('Q', boundaries=np.arange(qmin, qmax+dq/2., dq), unit='1./angstrom')
    eaxis = H.axis('E', boundaries=np.arange(emin, emax+de/2., de), unit='meV')
    hist = H.histogram('IQE', (qaxis, eaxis), data=data, errors=err2)
    if outfile.endswith('.nxs'):
        import warnings
        warnings.warn("reduce function no longer writes iqe.nxs nexus file. it only writes iqe.h5 histogram file")
        outfile = outfile[:-4] + '.h5'
    hh.dump(hist, outfile)
    return
