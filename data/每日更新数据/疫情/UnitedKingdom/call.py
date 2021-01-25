import pandas as pd
import os,datetime,time

def get_cumcase():
    date = '2020-10-08'
    start_date = datetime.datetime.strptime(date,'%Y-%m-%d')
    end_date = datetime.datetime.today() + datetime.timedelta(days=-1)

    while start_date < end_date:
        date = datetime.datetime.strftime(start_date,'%Y-%m-%d')
        print(date)
        url = 'https://api.coronavirus.data.gov.uk/v2/data?areaType=region&metric=cumCasesByPublishDate&format=csv&release={}'.format(date)
        z = 0
        while True:
            try:
                df = pd.read_csv(url)[['date','areaName','cumCasesByPublishDate']]
                break
            except Exception:
                z += 1
                print('请求失败')
                if z > 2:
                    print('1小时后请求')
                    time.sleep(3600)
                time.sleep(100)
        df = df.sort_values('areaName')
        df.to_csv('cumCase.csv',mode='a',index=0,header=0)
        start_date += datetime.timedelta(days=1)

def sort_case():
    df = pd.read_csv('cumCase.csv')
    df = df.sort_values(by=[0,1])
    df.to_csv('cumCase.csv',index=0)

def get_RD():
    url = 'https://api.coronavirus.data.gov.uk/v2/data?areaType=region&metric=cumDeathsByPublishDate&format=csv'
    df = pd.read_csv(url)[['date','areaName','cumDeathsByPublishDate']]
    df.columns = ['date','name','Deaths']
    df = df.sort_values(['date','name'])
    df.to_csv('Deaths.csv',index=0)

# sort_case()
# get_cumcase()
get_RD()