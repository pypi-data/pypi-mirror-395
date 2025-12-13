from MDUS.Class.DataClass import Data

from MDUS.LoadData import LoadMag
from MDUS.Plot import PlotMag
from MDUS.Plot import PlotOrbit
from MDUS.Analysis import DataShaping
from MDUS.Analysis import Model

class MagData(Data):
    def __init__(self):
        super().__init__()
        self.info["Data Type"] = "MAG"
    def Info(self):
        super().Info()
    # LoadData
    def LoadSetting(self,sec=1,unit="Rm") -> None:
        LoadMag.magsetting(self,sec,unit)
    def Load(self,start=None,end=None,orbit=None) -> None:
        LoadMag.magload(self,start,end,orbit)
    # Plot
    def PlotSetting(self,component={'Bx':'red','By':'blue','Bz':'green','|B|':'black'},
                    ylabel='Magnetic Field [nT]',
                    title = None) -> None:
        PlotMag.PlotSetting(self,component,ylabel,title)
    def Plot(self,start=None,end=None,fig=None,ax=None,fsize=(9,3)):
        fig, ax = PlotMag.Plot(self,start,end,fig,ax,fsize)
        return fig, ax
    def PlotOrbit(self,fig=None,ax=None,
                  plane='XY',coordinate='MSO'):
        fig, ax = PlotOrbit.PlotOrbit(self,fig,ax,plane,coordinate)
        return fig, ax
    # DataShaping
    def GetPos(self,unit='Rm') -> None:
        DataShaping.GetPos(self,unit)
    def CTransform(self,coordinate='MSM',mag=True,replace=False) -> None:
        DataShaping.CTransform(self,coordinate,mag,replace)
    def MoveAverage(self,window=3,component=None) -> None:
        DataShaping.MoveAverage(self,window,component)
    # Model
    def CalcModel(self, model="KT17",
                   Rsun=0.4, DI=50):
        Model.CalcModel(self, model, Rsun, DI)
