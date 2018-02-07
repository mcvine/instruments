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


__doc__ = """
convert scattereed neutrons to events (pixelID, tofChannelNo, prob)
intercepted by a detector system.
"""

__implementation__ = """
This script runs a mcvine instrument simulation script consisting
of two components, a neutron player and a detector system.

The neutron player replay the neutrons stored in a neutron
storage. Those neutrons were scattered off of a sample
in a neutron beam.

The detector system is specified by a xml file.
"""


cmd_help = __doc__


# main methods
def run(neutrons, workdir, nodes, ncount=None,
        tofbinsize=0.1, tofmax=0.2,
        instrument=None,
        detsys=None,
        z_rotation=0.):
    neutrons = os.path.abspath(neutrons)
    workdir = os.path.abspath(workdir)
    if os.path.exists(workdir):
        raise IOError("%s already exists" % workdir)
    os.makedirs(workdir)
    if not detsys:
        if not instrument:
            raise RuntimeError("Please specify instrument name or path to <instrument>.xml.fornxs")
        from mcvine import resources
        detsys = os.path.join(
            resources.instrument(instrument.upper()), 
            'detsys',
            '%s.xml.fornxs' % instrument)
    eventdat = sendneutronstodetsys(
        neutronfile=neutrons, workdir=workdir, nodes=nodes, ncount=ncount,
        tofbinsize=tofbinsize, tofmax=tofmax,
        detsys=detsys, z_rotation=z_rotation,
        )
    return


def sendneutronstodetsys(
    neutronfile=None, scattering_rundir=None, nodes=None, ncount=None,
    workdir = None, tofbinsize = None, tofmax=None, detsys = None,
    z_rotation = None,
    ):
    """
    run a simulation to send neutrons to det system
    
    workdir: directory where the simulation is run
    tofmax: unit: second
    tofbinsize: unit: microsecond
    
    z_rotation: angle of rotation applied to the detector system around z axis (vertical). unit: degree
    """
    # create workdir if it does not exist
    if not os.path.exists(workdir):
        os.makedirs(workdir)
        
    # number of neutrons scattered
    if not neutronfile:
        neutronfile = os.path.join(scattering_rundir, 'out', 'scattered-neutrons')
    if not ncount:
        from mcni.neutron_storage.idf_usenumpy import count
        ncount = count(neutronfile)
        
    # create simulation command
    cmd_name = 'sd'
    sim_cmd = os.path.join(workdir, cmd_name)
    open(sim_cmd, 'wt').write(sd_txt)
    
    
    # build command
    cmd = ['python '+cmd_name]
    args = {
        'source': 'NeutronFromStorage',
        'detsys': 'DetectorSystemFromXml',
        'output-dir': 'out',
        'detsys.tofparams': '0,%s,%s' % (tofmax, 1e-6*tofbinsize,), 
        'detsys.instrumentxml': detsys,
        'detsys.eventsdat': 'events.dat',
        'geometer.detsys': '(0,0,0),(0,%s,0)' % (z_rotation or 0,),
        'ncount': ncount,
        'source.path': neutronfile,
        }
    if nodes:
        from mcni.pyre_support.MpiApplication \
            import mpi_launcher_choice as launcher
        args['%s.nodes' % launcher] = nodes
    cmd += ['--%s=%s' % (k,v) for k,v in args.iteritems()]
    cmd = ' '.join(cmd)
    run_sh = os.path.join(workdir, 'run.sh')
    open(run_sh, 'w').write(cmd+'\n')
    execute(cmd, workdir)
    
    # events.dat
    outfile = os.path.join(workdir, 'out', 'events.dat')
    return outfile

sd_txt = """
import mcvine
from mcvine.applications.InstrumentBuilder import build
components = ['source', 'detsys']
App = build(components)
app = App('sd')
app.run()
"""


# utils
import os, subprocess as sp, shlex
def execute(cmd, workdir):
    print '* executing %s... ' % cmd
    args = shlex.split(cmd)
    p = sp.Popen(args, cwd=workdir)
    p.communicate()
    if p.wait():
        raise RuntimeError, "%r failed" % cmd
    return


import numpy as np
import os, subprocess as sp

#
# version
__id__ = "$Id$"

# End of file 


