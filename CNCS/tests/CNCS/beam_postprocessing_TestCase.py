#!/usr/bin/env python

from mcvine.instruments.CNCS import beam_postprocessing as bpp
import numpy as np, os
import histogram as H, histogram.hdf as hh

here = os.path.dirname(__file__)


import unittest

class TestCase(unittest.TestCase):

    def test1(self):
        Itof = H.histogram("itof", [('tof', np.arange(2000, 3000.), 'microsecond')])
        Itof.I[:] = 0; Itof.I[500] = 10
        dir = 'tmp.bpptest'
        if not os.path.exists(dir): os.makedirs(dir)
        hh.dump(Itof, os.path.join(dir, 'itof.h5'))
        print bpp.computeFWHM(dir)
        return


if __name__ == '__main__': unittest.main()
