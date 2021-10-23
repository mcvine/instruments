# -*- Python -*-
#
# Jiao Lin <jiao.lin@gmail.com>
#

"""
post processing routines for beam simulation
"""

from mcvine.instruments import dgs_bpp

LSAMPLE = 30.
Ei=2.63
m2sout = "m2sout"
out = "out.bpp"
dgs_bpp.run(m2sout, out, Ei, LSAMPLE)

# End of file
