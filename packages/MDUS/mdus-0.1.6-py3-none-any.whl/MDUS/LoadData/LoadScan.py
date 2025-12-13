from MDUS.LoadData import LoadFunction as ldf
from MDUS.Data.data import orbit as orbits
import MDUS.Constant.constant as cst
from MDUS.Convert.ConvertScan import scanconvert

import pandas as pd
import numpy as np

# from MDUS.Class.ScanDataClass import ScanData

def scansetting(self,target='Proton',quality=0) -> None:
    if quality < 0:
        quality = "All"
    if target not in ["start","stop","VE","Proton","EP"]:
        raise ValueError("target must be start, stop, VE, Proton, or EP")
    self.info["Target"] = target
    self.info["Quality"] = quality
# ScanData.LoadSetting = scansetting

def scanload(self,start=None,end=None,orbit=None) -> None:
        # 例外処理
    if start is None and end is None and orbit is None:
        raise ValueError("start, end, and orbit cannot be None at the same time")    

    # 時刻処理
    if orbit is not None:
        startdate = pd.to_datetime(orbits.query('index == @orbit')['MP1'].values[0])
        enddate = pd.to_datetime(orbits.query('index == @orbit')['MP4'].values[0])
    else:
        startdate,enddate = ldf.convert_to_datetime(start,end)

    # データ読み込み
    ofile = []
    pfile = []
    result = pd.DataFrame()

    # settingの読み込み
    if "Target" not in self.info.keys():
        target = "Proton"
        quality = 0
        self.info["Target"] = target
        self.info["Quality"] = quality
    else:
        target = self.info["Target"]
        quality = self.info["Quality"]


    # 読み込むファイルの取得
    years = []
    days = []
    for date in pd.date_range(startdate.date(),enddate.date(),freq="D"):
        year = date.year
        day = date.dayofyear
        years.append(year)
        days.append(day)
        pfile.append(ldf.found_pfile("FIPS_CDR_SCAN",year,day,target=target))
        tmp = ldf.found_ofile("FIPS_CDR_SCAN",year,day)
        if len(tmp) == 0:
            print("Warning: Cannot find original file")
            print("original data path may not be correct")
            print("Please check the datapath.json file")
            self.value = None
            return
        ofile.append(str(ldf.found_ofile("FIPS_CDR_SCAN",year,day)[-1]))
    
    # 読み込むファイルの取得
    for p, o, year, day in zip(pfile, ofile, years,days):
        try:
            df = pd.read_pickle(p)
            result = pd.concat([result,df])
        except FileNotFoundError:
            print("Warning: %s not found" % p)
            if len(ofile) == 0:
                print("Error: There is no data file. please downlad from PDS")
                self.value = None
                return 
            else:
                print("Found original file. Convert to pickle file")  
                df = scanconvert(o,p,target)
                result = pd.concat([result,df])
    if orbit is not None:
        self.info["Orbit"] = orbit
    self.info["Start Date"] = startdate
    self.info["End Date"] = enddate
    self.info["Original File"] = ofile
    self.info["Input File"] = pfile
    if quality != 'All':
        # result = result.query('quality <= @quality')
        result[cst.EQTAB] = result[cst.EQTAB].where(result['quality'] <= quality, np.nan)
    result = result.query('@startdate <= index <= @enddate')
    self.value = result

# ScanData.Load = scanload                         