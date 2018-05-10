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
        beam_out = os.path.join(datadir, 'beam-100meV', 'out')
        import shutil
        self.nxsfile_with_Eidata = 'arcs-sim-with-Eidata.nxs'
        self.nxsfile_without_Eidata = os.path.join(datadir, 'arcs-sim.nxs')
        shutil.copyfile(self.nxsfile_without_Eidata, self.nxsfile_with_Eidata)
        nxs.populate_Ei_data(beam_out, self.nxsfile_with_Eidata)
        self.qaxis = 0, 0.1, 13
        return
            
    
    def test1(self):
        nxsfile = self.nxsfile_with_Eidata
        nxs.reduce(nxsfile, self.qaxis, 'iqe1.h5', use_ei_guess=False, tof2E=True, ibnorm='ByCurrent', use_monitors=False)
        return

    def test2(self):
        nxsfile = self.nxsfile_without_Eidata
        with self.assertRaises(RuntimeError):
            nxs.reduce(nxsfile, self.qaxis, 'iqe2.h5', use_ei_guess=False, tof2E=True, ibnorm='ByCurrent', use_monitors=False)
        return

    def test3(self):
        nxsfile = nxs.nxsfilename_with_monitors(self.nxsfile_with_Eidata)
        nxs.reduce(nxsfile, self.qaxis, 'iqe3.h5', use_ei_guess=False, tof2E=True, ibnorm='ByCurrent', use_monitors=True)
        return

    def test4(self):
        nxsfile = self.nxsfile_without_Eidata
        nxs.reduce(nxsfile, self.qaxis, 'iqe4.h5', use_ei_guess=True, tof2E=True, ibnorm='ByCurrent', ei_guess=100., t0_guess=20.)
        return



if __name__ == '__main__': unittest.main()
