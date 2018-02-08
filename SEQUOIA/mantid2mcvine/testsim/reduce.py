from mantid import simpleapi as msa

ws = msa.Load('sim.nxs')
out = msa.DgsReduction(
    SampleInputWorkspace=ws,
    IncidentEnergyGuess=70.49, UseIncidentEnergyGuess=1,
    TimeZeroGuess=25.415)
msa.SofQW3(
        InputWorkspace='out',
        OutputWorkspace='iqw',
        QAxisBinning="0,0.1,12",
        EMode='Direct',
        )
msa.SaveNexus(
        InputWorkspace='iqw',
        Filename = 'iqe.nxs',
        Title = 'iqw',
        )

