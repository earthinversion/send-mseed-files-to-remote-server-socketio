from obspy import read
from glob import glob
import os


waveformLoc = "rfidget1"

all_waveform_data = glob(os.path.join(waveformLoc, "*.mseed"))

for wf in all_waveform_data:
    st = read(wf)

    print(st)

    del st
