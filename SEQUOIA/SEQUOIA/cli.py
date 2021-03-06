# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

import sys
import click
from ..cli import instruments
from mcvine.cli import pyre_app, alias

cmd_prefix = "mcvine instruments sequoia "

@instruments.group()
@alias("sequoia", cmd_prefix)
def sequoia():
    return

sequoia_app = lambda name: pyre_app(parent=sequoia, appname = name, cmd_prefix=cmd_prefix)

# beam sim
@sequoia_app("sequoia_analyze_beam")
def analyze_beam(ctx):
    from .applications import BeamAnalysis as mod
    return mod.App, mod.__file__

@sequoia_app('sequoia_moderator2sample')
def mod2sample(ctx):
    "moderator to sample simulation"
    from .applications import Moderator2Sample as mod
    return mod.App, mod.__file__

@sequoia_app('sequoia_m2s')
def m2s(ctx):
    "simplified moderator to sample simulation app"
    from .applications import M2S as mod
    return mod.App, mod.__file__

@sequoia_app('sequoia_beam')
def beam(ctx):
    "beam simulation. include mod2sample sim and post-processing"
    from .applications import Beam as mod
    return mod.App, mod.__file__


# detsys sim
@sequoia.command(help="""convert scattereed neutrons to nexus file

Impl.: mcvine.instruments.SEQUOIA.applications.Neutrons2Nxs
""")
@click.option("--neutrons", default="", help='path to neutron data file')
@click.option("--nxs", default="sequoia-sim.nxs", help='nexus output path')
@click.option("--workdir", default='work-sequoia-neutrons2nxs', help="working dir to save intermediate data fiels")
@click.option("--nodes", default=0)
@click.option("--populate-metadata/--no-populate-metadata", default=False)
@click.option("--beam", default="", help='beam simulation path. need only when populate-metadata is True')
@alias("sequoia_neutrons2nxs", "%s neutrons2nxs" % cmd_prefix)
@click.pass_context
def neutrons2nxs(ctx, neutrons, nxs, workdir, nodes, populate_metadata, beam):
    if not neutrons:
        click.echo(ctx.get_help(), color=ctx.color)
        return
    from .applications.Neutrons2Nxs import run
    run(neutrons, nxs, workdir, nodes)

    if populate_metadata:
        import os, shutil
        # save a copy
        base, ext = os.path.splitext(nxs)
        nometadata = base+"_no_metadata"+ext
        shutil.copyfile(nxs, nometadata)
        # populate
        from .applications import nxs as nxsmod
        beam_out = os.path.abspath(os.path.join(beam, 'out'))
        if sys.version_info < (3,0):
            nxs = nxs.encode()
        nxsmod.populate_Ei_data(beam_out, nxs)
    return


# nexus file utilities
@sequoia.group()
def nxs():
    "nexus utils"
    return

@nxs.command()
@click.option('--type', default="Ei", type=click.Choice(['Ei', 'monitor']), help='type of metadata')
@click.option('--beam_outdir', help='path to the output directory of sequoia beam simulation')
@click.option('--nxs', help='path to the nexus file to be decorated')
@alias("sequoia_nxs_populate_metadata", "%s nxs populate_metadata" % cmd_prefix)
@click.pass_context
def populate_metadata(ctx, type, beam_outdir, nxs):
    "populate metadata into the simulated nexus file"
    if not nxs or not beam_outdir:
        click.echo(ctx.get_help(), color=ctx.color)
        return
    from .applications import nxs as nxsmod
    f = getattr(nxsmod, "populate_%s_data" % type)
    f(beam_outdir, nxs)
    return

@nxs.command()
@click.argument("nxs")
@click.option('--out', default="iqe.nxs", help="output path. Eg. iqe.nxs")
@click.option('--use_ei_guess', default=False)
@click.option('--ei_guess', help='guess for Ei', default=0.)
@click.option('--qaxis', help='Qmin Qmax dQ', default=(0.,13.,0.1))
@click.option('--eaxis', help='Emin Emax dE', default=(0.,0.,0.))
@click.option('--tof2E/--no-tof2E', help='If true, input data must be tof events', default=None)
@click.option('--ibnorm',
              help='Incident beam normalization',
              type=click.Choice(['ByCurrent', 'ToMonitor', 'None']),
              default='ByCurrent')
@alias("sequoia_nxs_reduce", "%s nxs reduce" % cmd_prefix)
def reduce(nxs, out, use_ei_guess, ei_guess, qaxis, eaxis, tof2e, ibnorm):
    "run reduction"
    if ei_guess > 0:
        use_ei_guess = True
    if tof2e is None:
        tof2e = 'guess'

    qmin, qmax, dq = qaxis
    qaxis = (qmin, dq, qmax)
    
    import numpy as np
    if np.all(np.array(eaxis)==0.): eaxis = None
    if eaxis is not None:
        emin, emax, de = eaxis
        eaxis = emin, de, emax
    
    if sys.version_info < (3,0):
        nxs = nxs.encode("utf8"); out = out.encode("utf8")
        ibnorm = ibnorm.encode("utf8")
    print(("* tof2E=%s" % tof2e))
    d = dict(
        nxsfile = nxs,
        use_ei_guess = use_ei_guess,
        ei_guess = ei_guess,
        qaxis = qaxis,
        eaxis = eaxis,
        outfile = out,
        tof2E = tof2e,
        ibnorm = ibnorm,
        )
    from .applications.nxs import reduce
    reduce(**d)
    return


# End of file 
