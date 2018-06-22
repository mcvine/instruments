# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2008-2014  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

"""
post processing routines for hyspec beam simulation

post processing takes the output from hyspec_moderator2sample app "m2sout"
and generate better outputs in "out".
"""

# this is copied from hyspec_moderator2sample.instr
# XXX: duplicate code. will need to change this 
# XXX: if the instrument changes. 
L1 = 9.93 ;
L2 = 48. * 0.501 ;
L3 = 5.0 ;
LMM = L1 + L2 + L3 ; # moderator to monochromator


import os, time


def run(m2sout, out, Ei, LMS):
    """this is the main function for hyspec beam postprocessing
    it calls several sub-routines to perform a series of postprocesing
    steps.
    """
    # compute flux at sample position and make sure flux is nonzero
    flux = computeFlux(m2sout)
    # simulate spectra for fake monitors at sample position
    runMonitorsAtSample(Ei, LMS, m2sout, out)
    # move neutrons to output dir
    moveNeutronsToOutputDir(m2sout, out)
    # compute average incident energy at sample
    energy = computeAverageEnergy(out)
    # compute average tof at sample
    tof = computeAverageTof(out)
    # compute emission time
    from mcni.utils import conversion
    vi = conversion.e2v(energy)
    LSAMPLE = LMM + LMS
    t0 = tof - LSAMPLE/vi
    # compute fwhm of tof spetrum at sample
    fwhm = computeFWHM(out)
    fwhm *= 1e6 # convert to microsecond
    #
    props = {
        'flux': '%s counts per 34kJ pulse' % flux,
        'average energy': '%s meV' % energy,
        'average tof': '%s microsecond' % (tof*1e6),
        'tof fwhm': '%s microsecond' % fwhm,
        "emission time": '%s microsecond' % (t0*1e6),
        'monochromator-sample distance': "%s meters" % LMS,
        }
    open(os.path.join(out, 'props.json'), 'w').write(str(props))
    return


from ..ARCS.beam_postprocessing import computeFlux, computeAverageEnergy, computeAverageTof, computeFWHM, moveNeutronsToOutputDir, _exec


def runMonitorsAtSample(E, LMS, m2sout, out):
    from mcni.utils.conversion import e2v
    v = e2v(E)
    from pyre.units.time import second
    L = LMM + LMS
    t = L/v
    
    neutronfile = os.path.join(m2sout, 'neutrons')
    from mcni.neutron_storage.idf_usenumpy import count
    n = count(neutronfile)
    
    cmd = ['mcvine_analyze_beam']
    cmd += ['--output-dir=%s' % out]
    cmd += ['--ncount=%s' % n]
    cmd += ['--buffer_size=%s' % min(n, 1e6)]
    # XXX: -0.15 comes from the fact that the in hyspec_moderator2sample
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
    print 'Running beam monitors...'
    _exec(cmd)
    print 'done.'
    time.sleep(1)
    return


# End of file 
