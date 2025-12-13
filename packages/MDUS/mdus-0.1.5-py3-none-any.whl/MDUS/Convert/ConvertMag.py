import pandas as pd
import datetime

def magconvert(ofile,pfile,sec):
    tmp = pd.read_csv(ofile,header=None,sep='\s+')

    dates = []
    if sec == 'raw':
        for i in tmp.itertuples():
            year = i[1]
            totalday = i[2]
            hour = i[3]
            minutes = i[4]
            second = i[5]
            dates.append(pd.to_datetime(datetime.datetime(year,1,1) + datetime.timedelta(days=totalday-1,hours=hour,minutes=minutes,seconds=second)))
        timetag = list(tmp[5])
        msox = list(tmp[6])
        msoy = list(tmp[7])
        msoz = list(tmp[8])
        Bx = list(tmp[9])
        By = list(tmp[10])
        Bz = list(tmp[11])

        outdata = pd.DataFrame({'date':dates,'TIME_TAG':timetag,'X_MSO':msox,'Y_MSO':msoy,'Z_MSO':msoz,'Bx':Bx,'By':By,'Bz':Bz})
    else:
        for i in tmp.itertuples():
            year = i[1]
            totalday = i[2]
            hour = i[3]
            minutes = i[4]
            second = i[5]
            dates.append(pd.to_datetime(datetime.datetime(year,1,1) + datetime.timedelta(days=totalday-1,hours=hour,minutes=minutes,seconds=second))) 
        timetag = list(tmp[5])
        navg = list(tmp[6])   
        msox = list(tmp[7])
        msoy = list(tmp[8])
        msoz = list(tmp[9])
        Bx = list(tmp[10])
        By = list(tmp[11])
        Bz = list(tmp[12])
        DBx = list(tmp[13])
        DBy = list(tmp[14])
        DBz = list(tmp[15])

        outdata = pd.DataFrame({'date':dates,'TIME_TAG':timetag,'NAVG':navg,'X_MSO':msox,'Y_MSO':msoy,'Z_MSO':msoz,'Bx':Bx,'By':By,'Bz':Bz,'DBx':DBx,'DBy':DBy,'DBz':DBz})
    outdata = outdata.set_index('date')
    outdata.to_pickle(pfile)
    return outdata
    