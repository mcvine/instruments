import os, yaml
import mantid2mcvine as m2m

d = yaml.load(open("../SEQ_virtual.yml"))
im = m2m.InstrumentModel(**d)
