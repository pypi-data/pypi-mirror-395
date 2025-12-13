import pandas as pd
import numpy as np
import re

import MDUS.Constant.constant as cst

def scanconvert(ofile,pfile,target):
    # output
    result = {}
    targets = ["start","stop","VE","Proton","EP"]
    # データ読み込み
    tmp = pd.read_csv(ofile,skiprows=5,header=None,sep='\s+')
    # 日付計算
    dates = tmp[1].values
    years = np.array([date[:4] for date in dates]).astype('int')
    days = np.array([date[5:8] for date in dates]).astype('int')
    hours = np.array([date[9:11] for date in dates]).astype('int')
    minutes = np.array([date[12:14] for date in dates]).astype('int')
    seconds = np.array([date[15:17] for date in dates]).astype('int')
    mseconds = np.array([date[18:] for date in dates]).astype('int')

    dates = np.array([pd.to_datetime(f"{y}{d:03d}", format="%Y%j") for y, d in zip(years, days)]).astype('datetime64')
    time_deltas = hours.astype("timedelta64[h]") + \
                minutes.astype("timedelta64[m]") + \
                seconds.astype("timedelta64[s]") + \
                mseconds.astype("timedelta64[ms]")
    
    dates += time_deltas

    # qualityとmodeの取得
    quality = tmp[2].values
    modes = tmp[3].values

    # データの整形
    for i in range(len(targets)):
        indexnum = np.arange(4+i*64,68+i*64)
        temp = tmp[indexnum].copy()
        temp = temp.set_axis(cst.EQTAB[::-1],axis='columns')
        temp['date'] = dates
        temp['quality'] = quality
        temp['mode'] = modes
        temp = temp.set_index('date')
        result[targets[i]] = temp

        pfile = re.match(r"(.*/\d{4}_\d{3}_)", pfile).group(1)

        pfile_temp = pfile + targets[i] + '.pkl'

        # ファイル出力
        temp.to_pickle(pfile_temp)
    return result[target]