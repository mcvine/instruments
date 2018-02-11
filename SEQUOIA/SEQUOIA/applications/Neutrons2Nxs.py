#!/usr/bin/env python


"""
convert scattereed neutrons to nexus file.
"""

appname = 'sequoia-neutrons2nxs'
cmd_help = """
convert scattereed neutrons to nexus file.

Examples:

 $ sequoia-neutrons2nxs --neutrons=scattered-neutrons-example --nodes=2
"""


# main method
def run(neutrons, nxs, workdir, nodes, tofbinsize=0.1):
    from . import loadInstrumentModel
    im = loadInstrumentModel()
    im.tofbinsize = tofbinsize
    events = im.neutrons2events(neutrons, nodes=nodes, workdir=workdir)
    im.events2nxs(events, nxs)
    return
