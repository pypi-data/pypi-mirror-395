__version__ = "0.1.5"

# ---- below code is old version. ----
# spk file check
# import os
# import spiceypy as sp
# from MDUS.Data.spkdownload import DownloadSPK
# library_dir = os.path.dirname(__file__)
# spkernel_files = [
#     'msgr_040803_150430_150430_od431sc_2.bsp',
#     'msgr_dyn_v600.tf',
#     'naif0012.tls',
#     'pck00010_msgr_v23.tpc'
# ]
# def check_spkernel_files():
#     missing_files = []
#     for file in spkernel_files:
#         if not os.path.exists(os.path.join(library_dir, 'Data/spice_kernel', file)):
#             missing_files.append(file)
#         else:
#             sp.furnsh(str(os.path.join(library_dir, 'Data/spice_kernel', file)))
#     if missing_files:
#         print("Some spkernel files are missing")
#         print("You cannnot use some following functions:")
#         print("Missing files:")
#         for file in missing_files:
#             print("\t"+file)
# check_spkernel_files()

# --------------------------------------

# Spice setup
from MDUS.Spice.SpiceSetup import *
# check spk files
chech_spkfile()

# import data
from MDUS.Data.data import *

# import constant
from MDUS.Constant.constant import *

# import Classes
from MDUS.Class.MagDataClass import MagData
from MDUS.Class.ScanDataClass import ScanData
from MDUS.Class.DatasClass import Datas

# import LoadData
from MDUS.LoadData import LoadMag
from MDUS.LoadData import LoadScan
from MDUS.LoadData import LoadDatas

# import Plot
import MDUS.Plot.PlotMag
import MDUS.Plot.PlotOrbit
import MDUS.Plot.PlotScan
# import MDUS.Plot.PlotPchang
import MDUS.Plot.PlotDatas

# Analysis関連
from MDUS.Analysis import DataShaping
from MDUS.Analysis import Model
# from MDUS.Analysis import CalcPhysics

# import Convert
# from MDUS.Convert import ConvertMag