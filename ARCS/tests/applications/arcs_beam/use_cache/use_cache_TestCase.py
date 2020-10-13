#!/usr/bin/env python

import subprocess as sp, os, shlex

import unittest
class TestCase(unittest.TestCase):

    def test(self):
        workdir = os.path.abspath(os.path.dirname(__file__))
        cmd = "mcvine instruments arcs beam --keep-in-cache --use-cache -E=70 --ncount=4e6 --nodes=2"
        sp.check_call(shlex.split(cmd), shell=False, cwd=workdir)
        return

if __name__ == '__main__': unittest.main()

# End of file
