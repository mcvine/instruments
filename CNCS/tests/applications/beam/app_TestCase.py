#!/usr/bin/env python

import subprocess as sp, os, shlex

import unittest
class TestCase(unittest.TestCase):

    def test(self):
        workdir = os.path.abspath(os.path.dirname(__file__))
        workdir = os.path.join(workdir, '_work.beam_Ei5.1')
        if not os.path.exists(workdir):
            os.makedirs(workdir)
        sp.check_call(
            shlex.split("mcvine instruments cncs beam --E=5.1 --f1=60. --f2=60. --f3=60. --f41=300. --f42=300. --fluxmode=9.0 --ncount=2e6 --nodes=2"), 
            shell=False, cwd=workdir)
        return


if __name__ == '__main__': unittest.main()

# End of file 
