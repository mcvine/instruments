# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
post processing routines for beam simulation
post processing takes the output from sequoia-m2s app "m2sout"
and generate better outputs in "out".
"""

# These parameters should match the positions in sequoia-moderator2sample.
# The default values for them are in .../etc/sequoia_moderator2sample/sequoia_moderator2sample.pml
# distance from moderator to monitor1, unit meter
LM1 = 18.26
# distance from moderator to monitor2
LM2 = 29.0032

# distance to sample.
# This should match .../etc/sequoia_analyze_beam/sequoia_analyze_beam.pml
# It does not match the value in __init__.py but it is OK because
# we are just using this to calculate flux, average energy, average tof, tof fwhm, and emission time.
# Only the average TOF might be slightly off, and other values should be pretty accurate.
# The most important thing is probably that the emission time will be accurate.
# This has been this way for a long time so we don't want to change it to render
# the previous simulations not usable.
LSAMPLE = 20.0254


import os, time

def run(m2sout, out, Ei):
    """this is the main function for sequoia beam postprocessing
    it calls several sub-routines to perform a series of postprocesing
    steps.
    """
    flux = computeFlux(m2sout)
    # computed spectra for real monitors
    computeFocusedSpectraForRealMonitors(Ei, m2sout, out)
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
    # compute fwhm of energy spetrum at sample
    fwhm = computeFWHM(out)
    fwhm *= 1e6 # convert to microsecond
    props = {
        'flux': '%s counts per 34kJ pulse' % flux,
        'average energy': '%s meV' % energy,
        'tof fwhm': '%s microsecond' % fwhm,
        "emission time": '%s microsecond' % (t0*1e6),
        'average tof': '%s microsecond' % (tof*1e6),
        }
    open(os.path.join(out, 'props.json'), 'w').write(str(props))
    return


from ..ARCS.beam_postprocessing import computeFlux, computeAverageEnergy, computeAverageTof, computeFWHM, moveNeutronsToOutputDir, _exec


def runMonitorsAtSample(E, m2sout, out):
    from ..ARCS.beam_postprocessing import runMonitorsAtSample
    return runMonitorsAtSample(E, m2sout, out, L=LSAMPLE, instrument='sequoia')


def computeFocusedSpectraForRealMonitors(E, m2sout, out):
    from ..ARCS.beam_postprocessing import computeFocusedSpectraForRealMonitors
    return computeFocusedSpectraForRealMonitors(E, m2sout, out, LM1=LM1, LM2=LM2)


# End of file 
