# -*- Python -*-
#
#

"""
post processing routines for cncs beam simulation

post processing takes the output from cncs_moderator2sample app "m2sout"
and generate better outputs in "out".
"""

"""
Dev notes:

Bad implementation:
* hard-coded mod2sample distance and recorder-sample distance
"""

LSAMPLE = 36.264

import os, time


def run(m2sout, out, Ei):
    """this is the main function for cncs beam postprocessing
    it calls several sub-routines to perform a series of postprocesing
    steps.
    """
    # compute flux at sample position and make sure flux is nonzero
    flux = computeFlux(m2sout)
    # computed spectra for real monitors
    # computeFocusedSpectraForRealMonitors(Ei, m2sout, out)
    # simulate spectra for fake monitors at sample position
    runMonitorsAtSample(Ei, m2sout, out)
    # move neutrons to output dir
    moveNeutronsToOutputDir(m2sout, out)
    # compute average incident energy at sample
    energy = computeAverageEnergy(out)
    # compute average tof at sample
    tof = computeAverageTof(out)
    # compute emission time
    from mcni.utils import conversion
    vi = conversion.e2v(energy)
    t0 = tof - LSAMPLE/vi
    # compute fwhm of tof spetrum at sample
    fwhm = computeFWHM(out)
    fwhm *= 1e6 # convert to microsecond
    #
    props = {
        'flux': '%s counts per 34kJ pulse' % flux,
        'average energy': '%s meV' % energy,
        'tof fwhm': '%s microsecond' % fwhm,
        "emission time": '%s microsecond' % (t0*1e6),
        'average tof': '%s microsecond' % (tof*1e6),
        }
    open(os.path.join(out, 'props.json'), 'w').write(str(props))
    return


def computeFlux(m2sout):
    f = os.path.join(m2sout, 'neutrons')
    from mcni.neutron_storage.idf_usenumpy import totalintensity, count
    I = totalintensity(f)
    if I == 0:
        raise RuntimeError("There is no neutrons at sample position. Please increase ncount")
    # XXX: double check this
    # one MC run corresponds to 34kJ/pulse
    # this is the flux if the power is at 34kJ/pulse
    # unit: 1/34kJ pulse
    # every neutron in the storage represents one 34kJ pulse. so 
    # we need to normalize by number of events in the storage
    nevts = count(f)
    flux = I/nevts
    return flux


def computeAverageEnergy(out):
    from histogram.hdf import load
    h = load(os.path.join(out, 'ienergy.h5'), 'ienergy')
    e = (h.energy * h.I).sum()/h.I.sum()
    return e


def computeAverageTof(out):
    from histogram.hdf import load
    h = load(os.path.join(out, 'itof.h5'), 'itof')
    tof = (h.tof * h.I).sum()/h.I.sum()
    return tof


def computeFWHM(out):
    from histogram.hdf import load
    import numpy as np
    itof = load(os.path.join(out, 'itof.h5'), 'itof')
    max = itof.I.max()
    indmax = np.where(itof.I==max)[0][0]
    left = itof.I[:indmax+1]
    right = itof.I[indmax:]
    leftindex = np.where(left > max/2)[0][0]
    rightindex = np.where(right > max/2)[0][-1] + indmax
    fwhm = (1+rightindex-leftindex) * (itof.tof[1]-itof.tof[0])
    return fwhm


def runMonitorsAtSample(E, m2sout, out):
    from mcni.utils.conversion import e2v
    v = e2v(E)
    from pyre.units.time import second
    L = 36.264
    t = L/v
    
    neutronfile = os.path.join(m2sout, 'neutrons')
    from mcni.neutron_storage.idf_usenumpy import count
    n = count(neutronfile)
    
    cmd = ['mcvine_analyze_beam']
    cmd += ['--output-dir=%s' % out]
    cmd += ['--ncount=%s' % n]
    cmd += ['--buffer_size=%s' % min(n, 1e6)]
    # XXX: -0.15 comes from the fact that the in cncs_moderator2sample
    # XXX: the neutron storage is 0.15 before the sample position
    cmd += ['--geometer.source="((0,0,-0.15),(0,0,0))"']
    cmd += ['--source.path=%s' % neutronfile]
    # fix monitor params that depend on incident energy
    cmd += ['--monitor.mtof.tofmin=%s' % (t*0.9)]
    cmd += ['--monitor.mtof.tofmax=%s' % (t*1.1)]
    cmd += ['--monitor.mtof.ntof=%s' % (1000)]
    cmd += ['--monitor.menergy.energymin=%s' % (E*0.9)]
    cmd += ['--monitor.menergy.energymax=%s' % (E*1.1)]
    cmd += ['--monitor.menergy.nenergy=%s' % (1000)]
    cmd = ' '.join(cmd)
    print('Running beam monitors...')
    _exec(cmd)
    print('done.')
    time.sleep(1)
    return


# we don't have good simulation components
# for real monitors of CNCS yet.
# these were copied from ARCS
def computeFocusedSpectraForRealMonitors(E, m2sout, out):
    from mcni.utils.conversion import e2v
    v = e2v(E)
    from pyre.units.time import second
    import histogram.hdf as hh, histogram as H

    m1 = hh.load(os.path.join(m2sout, 'mon1-tof.h5'), 'I(tof)')
    L1 = 11.831
    t1 = L1/v #* second
    m1p = m1[(t1*0.9, t1*1.1)]
    m1pc = H.histogram('I(tof)', m1p.axes(), data=m1p.I, errors=m1p.E2)
    m1pc.setAttribute('title', 'Monitor 1 I(tof)')
    
    hh.dump(m1pc, os.path.join(out, 'mon1-itof-focused.h5'), '/', 'c')
    
    m2 = hh.load(os.path.join(m2sout, 'mon2-tof.h5'), 'I(tof)')
    L2 = 18.5
    t2 = L2/v #* second
    m2p = m2[(t2*0.9, t2*1.1)]
    m2pc = H.histogram('I(tof)', m2p.axes(), data=m2p.I, errors=m2p.E2)
    m2pc.setAttribute('title', 'Monitor 2 I(tof)')

    hh.dump(m2pc, os.path.join(out, 'mon2-itof-focused.h5'), '/', 'c')
    return


def moveNeutronsToOutputDir(m2sout, out):
    os.rename(
        os.path.join(m2sout, 'neutrons'),
        os.path.join(out, 'neutrons'),
        )
    return


def _exec(cmd):
    print((" -> running %s..." % cmd))
    import os
    if os.system(cmd):
        raise RuntimeError("%s failed" % cmd)


# End of file 
