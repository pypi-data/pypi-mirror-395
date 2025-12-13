import matplotlib.pyplot as plt
import matplotlib_inline.backend_inline
matplotlib_inline.backend_inline.set_matplotlib_formats("svg")
from matplotlib import dates as mdates
from matplotlib.colors import LogNorm
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np

from MDUS.Constant.constant import EQTAB
# from MDUS.Class import ScanDataClass

def Plot(self,start=None,end=None,fig=None,ax=None,fsize=(9,3),vmin=1e5,vmax=1e9):
    if fig is None or ax is None:
        fig, ax = plt.subplots(figsize=fsize
                              ,constrained_layout=True # 消すかも 
                               ) 
    if len(self.value.values) == 0:
        print("Warning: No plot data")
        return fig, ax
    if start is not None and end is not None:
        ds = pd.to_datetime(start)
        de = pd.to_datetime(end)
    else:
        ds = self.value.dropna().index[0]
        de = self.value.dropna().index[-1]   

    # dataの準備
    data_copy = self.value.copy()
    data_copy[EQTAB] = data_copy[EQTAB].replace(0,1e-38)
    pdata = data_copy[EQTAB].query('@ds <= index <= @de').values
    date = data_copy.query('@ds <= index <= @de').index.values

    # plot
    if not pdata.size == 0:
        cmap = plt.cm.jet
        cmap.set_under('white')
        cmap.set_bad('grey')
        hm = ax.pcolormesh(date,EQTAB,pdata.T,norm=LogNorm(vmin,vmax),cmap=cmap)
        hm.set_clim(vmin,vmax)
        ax.set_ylabel("Energy [keV/q]")
        # xlabel
        if 'X_MSO' in self.value.columns.values:
            ticks_labels = []
            for time in data_copy.query('@ds <= index <= @de').index:
                x = data_copy.loc[time, 'X_MSO']
                y = data_copy.loc[time, 'Y_MSO']
                z = data_copy.loc[time, 'Z_MSO']
                label = f"{time.strftime('%H:%M')}\n{x:.2f}\n {y:.2f}\n {z:.2f}"
                ticks_labels.append(label)
            ticks_labels = np.array(ticks_labels)
            ticks_num = np.linspace(0,len(ticks_labels)-1,6).astype(int)
            ax.set_xticks(data_copy.query('@ds <= index <= @de').index.values[ticks_num])
            ax.set_xticklabels(ticks_labels[ticks_num])
            # ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=6))
            ax.set_xlabel("UTC and Coordinate")
        else:
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
            ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=6))
            ax.set_xlabel("UTC")
        # settings
        ax.set_yscale('log')
        ax.set_ylim(0.2,20)
        ax.set_title(ds.strftime("%Y/%m/%d %H:%M:%S") + " - " + de.strftime("%Y/%m/%d %H:%M:%S"))
        cbar = plt.colorbar(hm)
        cbar.set_label(f"$1/s\cdot(keV/e)\cdot cm^2$")
    else:
        print("Warning: No plot data")
    return fig, ax
# ScanDataClass.ScanData.Plot = Plot