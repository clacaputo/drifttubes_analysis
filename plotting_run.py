###
### UNDER CONSTRUCTION

import uproot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import figure

import os

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input", type=str, required=True, help="root files" )

args = parser.parse_args()
input = args.input





df_w = pd.read_pickle(input)
totevents = df_w.shape[0]



def plotSigInEvent(eventNumber = 0):
    channel_map_color = {
     "ch0" : "b",
     "ch1" : "b",
     "ch2" : "b",
     "ch3" : "b",
     "ch4" : "black",
     "ch5" : "black",
     "ch6" : "black",
     "ch7" : "black",
     "ch8" : "black",
     "ch9" : "black",
     "ch10" : "maroon",
     "ch11" : "maroon",
     "ch12" : "maroon",
     "ch13" : "darkorange",
     "ch14" : "darkorange",
     "ch15" : "darkorange"
    }
    if (eventNumber > df_w.shape[0]):
        print("Event Number out of range")
        return -90
    fig = figure.Figure(figsize=(24,20))
    axs = fig.subplots(4,4)  #, sharex="all", sharey="all")
    for ch in np.arange(0,15):
        Row = int(ch / 4)
        Column = ch % 4
        ax = axs[Row][Column]
        
        w = np.array(df_w[f"ch{ch}"][eventNumber]) - 0.45
        t = np.array(df_t[f"ch{ch}"][eventNumber])# np.linspace(0,8.5e-7,1024)
        
        relmin = spsig.argrelmin(w,order=50)
        #print(w,relmin)
        _ = ax.plot(t,w, channel_map_color[f"ch{ch}"])
        ax.set_ylim(-0.22,0.1)
        ax.tick_params(direction='in', length=6, width=1.1, colors='k',
                      grid_color='k', which='major')
        ax.tick_params(direction='in', length=3, width=1, colors='k',
                      grid_color='k', which='minor')
        ax.grid(ls='--',color='grey')

    return fig


import matplotlib.backends.backend_pdf
outpath = "PLOTS"
pdf = matplotlib.backends.backend_pdf.PdfPages(os.path.join(outpath,f"{name}.pdf"))

for ev in np.arange(0,totevents):
    update_progress(ev/totevents, f"Plotting")
    txt = f'Event={ev+1}'
    fig = plotSigInEvent(ev)
    fig.suptitle(txt)
    plt.text(0.05,0.95,txt, transform=fig.transFigure, size=24)
    #fig.savefig(os.path.join(outpath,"event_{0}.png".format(ev+1)))
    pdf.savefig( fig )
    plt.close()
pdf.close()