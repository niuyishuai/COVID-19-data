import pandas as pd
import os,datetime

def get_distance():
    date = '20200224'
    start_date = datetime.datetime.strptime(date,'%Y%m%d')
    filename = './dati-regioni/dpc-covid19-ita-regioni-20200224.csv'

    df = pd.read_csv(filename)[['denominazione_regione','lat','long']]
    province_list = list(df['denominazione_regione'])
    while 'In fase di definizione/aggiornamento' in province_list:
        province_list.remove('In fase di definizione/aggiornamento')
    df = df[df['denominazione_regione'].isin(province_list)]

    distance = pd.DataFrame(columns=list(df['denominazione_regione']))
    distance.insert(0,'',df['denominazione_regione'])

    for index1 in df.index:
        for index2 in df.index:
            distance.at[index1,df.at[index2,'denominazione_regione']] = 1 / ((df.at[index1,'lat']-df.at[index2,'lat']) ** 2 + (df.at[index1,'long']-df.at[index2,'long']) ** 2)
    distance.to_csv('distance_region.csv',index=0)

def delete_lastrow(i):
    index = list(i.index)
    unknown = i.at[index[-1],'totale_casi']
    add = [unknown//(len(index)-1) for j in range(len(index)-1)]
    add[-1] = unknown - (len(index)-2) * (unknown//(len(index)-1))
    ddf = i.drop([index[-1]])
    ddf['totale_casi'] = ddf['totale_casi'] + add
    return ddf

def get_province_data():

    date = '20200224'
    datehave = '20210119'
    start_date = datetime.datetime.strptime(date,'%Y%m%d')
    end_date = datetime.datetime.strptime(datehave,'%Y%m%d')
    data = pd.DataFrame(columns=[])

    while start_date <= end_date:
        date = datetime.datetime.strftime(start_date,'%Y%m%d')
        filename = './dati-province/dpc-covid19-ita-province-{}.csv'.format(date)

        data_date = pd.DataFrame(columns=[])
        df = pd.read_csv(filename)[['denominazione_regione','denominazione_provincia','totale_casi']].groupby('denominazione_regione')
        for i in df:
            ddf = delete_lastrow(i[-1])
            if i[-1].at[list(i[-1].index)[-2],'denominazione_provincia'] == 'Fuori Regione / Provincia Autonoma':
                ddf = delete_lastrow(ddf)
            ddf = ddf.drop(['denominazione_regione'],axis=1).set_index('denominazione_provincia')
            data_date = pd.concat([data_date,ddf])
        data_date.columns = [date]
        data = pd.concat([data,data_date],axis=1)
        start_date += datetime.timedelta(days=1)
    print(data.T)
    data.T.to_csv('province.csv')

def get_region_data():
    date = '20200224'
    datehave = '20210119'
    start_date = datetime.datetime.strptime(date,'%Y%m%d')
    end_date = datetime.datetime.strptime(datehave,'%Y%m%d')
    data = pd.DataFrame(columns=[])

    while start_date <= end_date:
        date = datetime.datetime.strftime(start_date,'%Y%m%d')
        filename = './dati-regioni/dpc-covid19-ita-regioni-{}.csv'.format(date)

        df = pd.read_csv(filename)[['denominazione_regione','dimessi_guariti','deceduti','totale_casi']]
        df = df.set_index('denominazione_regione')
        df[date] = df['totale_casi'] - df['dimessi_guariti'] - df['deceduti']
        df = df.drop(['dimessi_guariti','deceduti','totale_casi'],axis=1)
        data = pd.concat([data,df],axis=1)
        start_date += datetime.timedelta(days=1)
    print(data.T)
    data.T.to_csv('region.csv')





get_distance()
# get_province_data()
# get_region_data()