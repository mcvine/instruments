# -*- Python -*-
#
#

"""
converte events.dat to nexus file.

events.dat are generated by mcvine simulation that sends scattereted neutrons
to a detector system.

"""

def run(eventfile, tofbinsize, nxsfile, type, instrument):
    print((eventfile, nxsfile))
    from mccomponents.detector.event_utils import readEvents
    events = readEvents(eventfile)
    
    prefix = 'mcvine.instruments.%s.nxs' % instrument.upper()
    mod = '%s.%s' % (prefix, type)
    mod = __import__(mod, fromlist = [''])
    mod.write(events, tofbinsize, nxsfile)
    return

# End of file 
