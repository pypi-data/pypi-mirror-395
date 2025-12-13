import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches
# from MDUS.Class import MagDataClass

theta = np.arange(0,2*np.pi+0.01,0.01)

def PlotOrbit(self,fig=None,ax=None,
              plane='XY',coordinate='MSO'):
    if fig is None or ax is None:
        fig, ax = plt.subplots(figsize=(6,6))
        ax.invert_xaxis()
        ax.set_xlim(2,-2)
        ax.set_ylim(-2,2)
        ax.set_aspect('equal')
    if 'X' in plane:
        if coordinate == 'MSM' or coordinate == 'aMSM' :
            w = patches.Wedge((0,-0.2),1,theta1=90,theta2=270,color='black')
        else:
            w = patches.Wedge((0,0),1,theta1=90,theta2=270,color='black')
        ax.add_patch(w)
    if plane == 'XZ' and (coordinate == 'MSM' or coordinate == 'aMSM'):
        ax.plot(np.cos(theta),np.sin(theta)-0.2,color='black',zorder=-1)
    else:
        ax.plot(np. cos(theta),np.sin(theta),color='black',zorder=-1)
    coor1 = plane[0] + '_' + coordinate
    coor2 = plane[1] + '_' + coordinate
    if not coor1 in self.value.columns:
        raise ValueError("Error: No Coordinate Data")
    ax.plot(self.value[coor1].values,self.value[coor2].values,color='red')
    ax.set_xlabel(coor1 + ' [Rm]')
    ax.set_ylabel(coor2 + ' [Rm]')
    return fig, ax

# MagDataClass.MagData.PlotOrbit = PlotOrbit