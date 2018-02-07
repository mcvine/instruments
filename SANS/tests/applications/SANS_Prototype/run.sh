#!/usr/bin/env bash
packetsize=1000
ncount=5e5
buffersize=1000

rm -rf neutrons.dat && SANS_Prototype.py --neutron_recorder.packetsize=$packetsize -ncount=$ncount -buffer_size=$buffersize -overwrite-datafiles
