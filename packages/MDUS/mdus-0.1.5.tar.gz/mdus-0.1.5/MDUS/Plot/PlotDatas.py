import matplotlib.pyplot as plt
import matplotlib_inline.backend_inline
matplotlib_inline.backend_inline.set_matplotlib_formats("svg")
import pandas as pd

# from MDUS.Class import DatasClass

def Plot(self,start=None,end=None,fig=None,ax=None,fsize=None,background=False):
    dtype = self.info["Load Success"]
    # ds, de
    if start is not None and end is not None:
        ds = pd.to_datetime(start)
        de = pd.to_datetime(end)    
    else:
        dss = []
        des = []
        for d in dtype:
            dss.append(self.value[d].value.dropna().index.values[0])
            des.append(self.value[d].value.dropna().index.values[-1])
        ds = min(dss)
        de = max(des)
    # fig, ax
    if fsize is None:
        fsize = (9,3*len(dtype))
    if fig is None or ax is None:
        fig, ax = plt.subplots(nrows=len(dtype),figsize=fsize,sharex=True,constrained_layout=True)
    for i in range(len(dtype)):
        if background:
            if dtype[i] == "FIPS_CDR_SCAN":
                ax[i].set_facecolor('grey')
        self.value[dtype[i]].Plot(fig=fig,ax=ax[i],start=ds,end=de)
    plt.grid(False)
    return fig, ax

# DatasClass.Datas.Plot = Plot