# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
post processing routines for DGS beam simulation
"""

# distance to sample.
import os, time, shutil
here = os.path.dirname(__file__)
here = os.path.abspath(here)

def run(m2sout, out, Ei, LSAMPLE):
    """this is the main function for arcs beam postprocessing
    it calls several sub-routines to perform a series of postprocesing
    steps.
    """
    # compute flux at sample position and make sure flux is nonzero
    flux = computeFlux(m2sout)
    # simulate spectra for fake monitors at sample position
    runMonitorsAtSample(Ei, m2sout, out, LSAMPLE)
    # copy neutrons to output dir
    copyNeutronsToOutputDir(m2sout, out)
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
    left = itof.I[:indmax]
    right = itof.I[indmax:]
    leftindex = np.where(left > max/2)[0][0]
    rightindex = np.where(right > max/2)[0][-1] + indmax
    fwhm = (rightindex-leftindex) * (itof.tof[1]-itof.tof[0])
    return fwhm


def runMonitorsAtSample(E, m2sout, out, L):
    from mcni.utils.conversion import e2v
    v = e2v(E)
    from pyre.units.time import second
    t = L/v

    neutronfile = os.path.abspath(os.path.join(m2sout, 'neutrons'))
    from mcni.neutron_storage.idf_usenumpy import count
    n = count(neutronfile)

    # cmd = ['mcvine instruments %s analyze_beam' % instrument]
    app = os.path.join(here, 'dgs_bpp_analyze_beam.py')
    # create a temp dir to run the simulation
    import tempfile
    tmpd = tempfile.mkdtemp()
    def copy2tmpd(fn):
        src = os.path.join(here, fn)
        dest = os.path.join(tmpd, fn)
        shutil.copyfile(src, dest)
    copy2tmpd('dgs_bpp_analyze_beam.pml')
    copy2tmpd('beam_analyzer.odb')
    cmd = ['python {}'.format(app)]
    cmd += ['--output-dir=%s' % os.path.abspath(out)]
    cmd += ['--ncount=%s' % n]
    cmd += ['--buffer_size=%s' % min(n, int(1e6))]
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
    from mcvine.run_script import _exec
    print(cmd, tmpd)
    _exec(cmd, cwd=tmpd)
    print('done.')
    time.sleep(1)
    # shutil.rmtree(tmpd)
    return

def copyNeutronsToOutputDir(m2sout, out):
    shutil.copyfile(
        os.path.join(m2sout, 'neutrons'),
        os.path.join(out, 'neutrons'),
        )
    return

# End of file
