import uproot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input", type=str, required=True, help="root files" )
#parser.add_argument("--voltage", action='store_true', help='Submit skimming only for background samples')
#parser.add_argument("--skipSignals", action='store_true', help='Submit skimming skipping signals samples')
#parser.add_argument("--voltage", type=str, required=True, choices=["m20","m10","nominal","p10","p20","all"], nargs='*',
#                                help="Group of voltage configuration [m20, m10, nominal, p10, p20, all]" )

args = parser.parse_args()
input = args.input
#voltage = args.voltage

global timewindow

channel_map_waves = {
     "ch0" : [],
     "ch1" : [],
     "ch2" : [],
     "ch3" : [],
     "ch4" : [],
     "ch5" : [],
     "ch6" : [],
     "ch7" : [],
     "ch8" : [],
     "ch9" : [],
     "ch10" : [],
     "ch11" : [],
     "ch12" : [],
     "ch13" : [],
     "ch14" : [],
     "ch15" : []
}

print(f"Opnening file: {input}")

with uproot.open(input) as file:
    totevents = len(file.keys())

    print(f"File open: {input}")
    for ev in np.arange(0,totevents):
        if ev % 100 == 0:
            print(ev,"out of - ",totevents)
        for ch in np.arange(0,16):
            waveform = file[f"Event{ev}"][f"Wafeform{ch}"].array()[0]
            #timewindow = file[f"Event{ev}"][f"Time{ch}"].array()[0]
            channel_map_waves[f"ch{ch}"].append(waveform)

    #print(len(timewindow))
    df_w = pd.DataFrame.from_dict(channel_map_waves)
    #df_w.assign(time = timewindow)
    outputname = input.split(".")[0]
    df_w.to_pickle(f"{outputname}.pkl")