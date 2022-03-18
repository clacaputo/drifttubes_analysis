import uproot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import json

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input", type=str, required=True, help="pkl files" )

args = parser.parse_args()
input = args.input
absPath, pklFileName = os.path.split(input)
jsonFileName = pklFileName.split('.')[0]+".json"

df_w = pd.read_pickle(input)
## Invert signal polarity and add offset
offset = 0 
if df_w.ch0[0][1] > 0.4:
    offset = 0.45
df_w = -(df_w) + offset


chs_1cm = ["ch4", "ch5", "ch6", "ch7", "ch8", "ch9"]
chs_3cm = ["ch13", "ch14"]
chs_2cm = ["ch10", "ch11", "ch12"]
chs_all = chs_1cm + chs_2cm + chs_3cm

print(f"Opening: {input}")
## Adding signal features
for ch in df_w.columns:
    if chs_all.count(ch):
        #print(ch)
        df_w[f"{ch}_ampl"] = df_w[ch].map(lambda x: np.array(x).max())
        df_w[f"{ch}_int"] = df_w[ch].map(lambda x: np.array(x).sum())
        #df_w[f"{ch}_baseline"] = df_w[ch].map(lambda x: x.sum()*0.01)
        df_w[f"{ch}_rms"] = df_w[ch].map(lambda x: np.sqrt(np.square(np.array(x)).mean() - np.square(np.array(x).mean())))




# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html#scipy-optimize-curve-fit
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.moyal.html#scipy.stats.moyal
import scipy.optimize as optimizer
import scipy.stats as stat

def landau(x, A, B, C):
    return A* stat.moyal.pdf(x, B, C)

fig = plt.figure(figsize=(18,12))
axs = fig.subplots(3,4)

fits_dict = {}

fitparamfile = open(os.path.join(absPath, jsonFileName),"w")

print(f"Fitting Landau for: {input}")
for num, ch in enumerate(chs_all):
    Row = int(num / 4)
    Column = num % 4
    ax = axs[Row][Column]
    singleFit_dict = {}

    mask_baseline = df_w[ch].map(lambda x: np.array(x[1:-1]).max()) > 0.03
    df_series_max = df_w[ch].map(lambda x: np.array(x[1:-1]).max())
    alpha = 4
    loc = 0.058
    scale = 7e-3
    # Plot histogram
    yval, xval, p = ax.hist(df_series_max[mask_baseline], bins=np.linspace(0,0.35,30), histtype="step", label=f"{ch} max distribution")
    ax.plot(xval[:-1]+(xval[1]/2),yval, '.')
    #plt.plot(np.linspace(0,0.35,50), landau(np.linspace(0,0.35,50), alpha, loc, scale),'r-')

    # Fitting to Landau
    popt, popc = optimizer.curve_fit(landau,  xval[:-1]+(xval[1]/2), yval, p0=[alpha, loc, scale])
    # Plot Landau
    ax.plot(np.linspace(0,0.35,100), landau(np.linspace(0,0.35,100), *popt), 'r-',
             label='fit: A=%2.5f,\nB=%2.5f,\nC=%2.5f' % tuple(popt))
    ax.set_xlabel('Amplitude [V]')
    ax.set_ylabel('Entries')
    ax.legend()
    singleFit_dict["mean"] = df_series_max[mask_baseline].mean()
    singleFit_dict["A"] = popt[0]
    singleFit_dict["B"] = popt[1]
    singleFit_dict["C"] = popt[2]
    #fitparamfile.write(f"{ch} - media {df_series_max[mask_baseline].mean()}\n")
    #fitparamfile.write('fit: A=%2.5f, B=%2.5f, C=%2.5f \n' % tuple(popt))
    ax.set_xlim(0,0.35)
    fits_dict[ch] = singleFit_dict

outputname = input.split(".")[0]
figtitle   = outputname.split("/")[-1]
fig.suptitle(figtitle)
fig.savefig(f"{outputname}_LANDAU.png")
#fitparamfile.close()
json.dump(fits_dict, fitparamfile, indent=6)

print(f"Image saved: {outputname}_LANDAU.png")
print("DONE!")