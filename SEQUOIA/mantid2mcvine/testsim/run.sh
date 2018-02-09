rm -rf mysim

set -e

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
python createnxs.py

# reduce
python reduce.py
mcvine mantid extract_iqe iqe.nxs ieq.h5
python -c "import histogram.hdf as hh; iqe=hh.load('ieq.h5').transpose(); hh.dump(iqe, 'iqe.h5')"
