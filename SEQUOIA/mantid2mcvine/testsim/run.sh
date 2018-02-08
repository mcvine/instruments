rm -rf mysim
mcvine workflow powder --instrument=SEQUOIA --sample=V --workdir=mysim

# beam
cd mysim/beam
echo "mcvine instruments sequoia beam -E=70 --ncount=1e8 --nodes=20" > run-beam.sh
time ./run-beam.sh
cd -

# fix sample kernel
cp V-scatterer.xml mysim/sampleassembly

# run sim
cd mysim
make NCOUNT=1e7 NODES=20 out/scattered-neutrons
cd -

# create NXS
python -c "from model import im; events = im.neutrons2events('mysim/out/scattered-neutrons', nodes=20); im.events2nxs(events, 'sim.nxs')"

# reduce
python reduce.py
mcvine mantid extract_iqe iqe.nxs iqe.h5
