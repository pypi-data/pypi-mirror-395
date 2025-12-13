from MDUS.Setting.setting import setting

import pandas as pd
from pathlib import Path

# 文字列日付をpandasのdatetime型へ変換する関数
def convert_to_datetime(start,end):
    try:
        start = pd.to_datetime(start)
        end = pd.to_datetime(end)
    except ValueError:
        raise ValueError("Error: start and end must be in the format of YYYY-MM-DD HH:MM:SS")
    if start > end:
        start,end = end,start
    return start,end

def found_pfile(datatype,year,day,sec=None,target=None):
    if datatype == "MAG":
        if sec == 'raw':
            pfile_tmp = str(year)+"_"+str(day).zfill(3)+"_raw.pkl"
        else:
            pfile_tmp = str(year)+"_"+str(day).zfill(3)+"_"+str(sec).zfill(2)+".pkl"
    elif datatype == "FIPS_CDR_SCAN":
        pfile_tmp = str(year) + "_" + str(day).zfill(3) + "_" + target + ".pkl"
    pfile_path = setting[datatype]["pfile_path"] + "/" + pfile_tmp
    return pfile_path

def found_ofile(datatype,year,day,sec=None):
    if datatype == "MAG":
        if sec == "raw":
            ofile_tmp = "MAGMSOSCI" + str(year-2000) + str(day).zfill(3)
        else:
            ofile_tmp = "MAGMSOSCIAVG" + str(year-2000)+str(day).zfill(3)+"_"+str(sec).zfill(2)
    elif datatype == "FIPS_CDR_SCAN":
        ofile_tmp = "FIPS_R" + str(year) + str(day).zfill(3) + "CDR"
    ofile_dir = Path(setting[datatype]["ofile_path"])
    ofile_path = [file for file in ofile_dir.rglob("*") if file.is_file() and ofile_tmp in file.name and 'TAB' in file.name]
    return ofile_path