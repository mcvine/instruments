from model import im
events = im.neutrons2events('mysim/out/scattered-neutrons', nodes=20)
im.events2nxs(events, 'sim.nxs')
