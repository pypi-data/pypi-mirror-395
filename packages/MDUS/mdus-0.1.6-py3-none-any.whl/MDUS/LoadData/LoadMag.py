from MDUS.LoadData import LoadFunction as ldf
from MDUS.Convert.ConvertMag import magconvert
from MDUS.Data.data import orbit as orbits
import MDUS.Constant.constant as cst

import pandas as pd
import numpy as np

# from MDUS.Class.MagDataClass import MagData

def magsetting(self,sec=1,unit="Rm") -> None:
    if sec not in [1,5,10,60,'raw']:
        raise ValueError("sec must be 1, 5, 10, 60 or 'raw'")
    else:
        self.info["Second"] = sec
    
    if unit not in ["Rm","km"]:
        raise ValueError("unit must be Rm or km")
    else:
        self.info["Unit"] = unit
# MagData.LoadSetting = magsetting

def magload(self,start=None,end=None,orbit=None) -> None:
    # 例外処理
    if start is None and end is None and orbit is None:
        raise ValueError("start, end, and orbit cannot be None at the same time")    

    # 時刻処理
    if orbit is not None:
        startdate = pd.to_datetime(orbits.query('index == @orbit')['BS1'].values[0])
        enddate = pd.to_datetime(orbits.query('index == @orbit')['BS4'].values[0])
    else:
        startdate,enddate = ldf.convert_to_datetime(start,end)

    # データ読み込み
    ofile = []
    pfile = []
    result = pd.DataFrame()

    # settingの読み込み
    if "Second" not in self.info.keys():
        sec = 1
        unit = "Rm"
        self.info["Second"] = sec
        self.info["Unit"] = unit
    else:
        sec = self.info["Second"]
        unit = self.info["Unit"]

    # 読み込むファイルの取得
    years = []
    days = []
    for date in pd.date_range(startdate.date(),enddate.date(),freq="D"):
        year = date.year
        day = date.dayofyear
        years.append(year)
        days.append(day)
        pfile.append(ldf.found_pfile("MAG",year,day,sec))
        tmp = ldf.found_ofile("MAG",year,day,sec)
        if len(tmp) == 0:
            print("Warning: Cannot find original file")
            self.value = None
            return
        ofile.append(str(ldf.found_ofile("MAG",year,day,sec)[-1]))

    # ファイル読み込み
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
                df = magconvert(o,p,sec)
                result = pd.concat([result,df])
    result['|B|'] = np.sqrt(np.array(result['Bx'].values) ** 2 + np.array(result['By'].values) ** 2 + np.array(result['Bz'].values) ** 2)
    result = result.query('@startdate <= index <= @enddate')

    if self.info["Unit"] == "Rm":
        result.loc[:,'X_MSO'] /= cst.Rm
        result.loc[:,'Y_MSO'] /= cst.Rm
        result.loc[:,'Z_MSO'] /= cst.Rm
    if orbit is not None:
        self.info["Orbit"] = orbit
    self.info["Start Date"] = startdate
    self.info["End Date"] = enddate
    self.info["Original File"] = ofile
    self.info["Input File"] = pfile
    self.value = result     
# MagData.Load = magload