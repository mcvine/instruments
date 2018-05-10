#!/usr/bin/env python

from mcvine.instruments.ARCS.applications import nxs
import numpy as np, os

here = os.path.dirname(__file__)
datadir = os.path.abspath(os.path.join(here, '..', '..', 'data'))


import unittest

class TestCase(unittest.TestCase):

    def setUp(self):
        fn = 'arcs-sim.nxs'
        if not os.path.exists(os.path.join(datadir, fn)):
            gzfile = os.path.join(datadir, fn+'.gz' )
            if not os.path.exists(gzfile):
                raise IOError("%s does not exist" % gzfile)
            cmd = 'cd %s; gunzip %s.gz' % (datadir, fn)
            if os.system(cmd):
                raise RuntimeError("%s failed" % cmd)
        return
            
    
    def test1(self):
        beam_out = os.path.join(datadir, 'beam-100meV', 'out')
        import shutil
        no_Eidata = 'arcs-sim-with-Eidata.nxs'
        shutil.copyfile(os.path.join(datadir, 'arcs-sim.nxs'), no_Eidata)
        nxs.populate_Ei_data(beam_out, no_Eidata)
        return


if __name__ == '__main__': unittest.main()
