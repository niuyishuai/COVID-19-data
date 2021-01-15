import pandas as pd
import datetime,os

def update_US():
    savefile = 'C:\\Users\\HUAWEI\\Documents\\GitHub\\COVID-19-data\\data\\每日更新数据\\疫情\\JohnHopkins\\data\\US\\country.csv'
    df = pd.read_csv(savefile)
    start_date = df.values[-1][0]

    date = datetime.datetime.strptime(start_date,'%m/%d/%Y') + datetime.timedelta(days=1)
    start_date = datetime.datetime.strftime(date,'%m-%d-%Y')
    filename = start_date + '.csv'

    while os.path.exists(filename):
        df = pd.read_csv(filename)[['Confirmed','Deaths','Recovered']].sum().to_frame().transpose().astype(int)
        df.insert(0,'Date',datetime.datetime.strftime(date,'%m/%d/%Y'))
        df['CurrentConfirmed'] = df['Confirmed'] - df['Deaths'] - df['Recovered']
        df.to_csv(savefile,mode='a',index=0,header=0)
        date += datetime.timedelta(days=1)
        start_date = datetime.datetime.strftime(date,'%m-%d-%Y')
        filename = start_date + '.csv'

if __name__ == "__main__":
    update_US()