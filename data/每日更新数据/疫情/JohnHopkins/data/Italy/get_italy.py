import pandas as pd
import os,datetime,json

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

def combine_matrix():
    # # step1 -- get region_province.json (need to fix one value by hand)
    # df = pd.read_csv('./dati-province/dpc-covid19-ita-province-20200224.csv').groupby('denominazione_regione')
    # province_region = {}
    # for i in df:
    #     for province in list(i[1]['denominazione_provincia']):
    #         if province != 'In fase di definizione/aggiornamento':
    #             province_region[province] = i[0]
    # with open('region_province.json','w') as f:
    #     json.dump(province_region,f)

    # step2 -- sum matrix from province to region
    with open('region_province.json','r') as f:
        province_region = json.load(f)
    data_id = pd.read_csv('./id_provinces_it.csv')
    province_id = dict(zip(data_id['COD_PROV'],data_id['DEN_PCM']))
    
    data = pd.read_csv('od_matrix_daily_flows_norm_full_2020_01_18_2020_06_26.csv')
    nums = list(data['p2'])
    for i in nums:
        data['p2'] = data['p2'].replace(i,province_region[province_id[i]])
    group = data.groupby(['p1','p2']).sum()
    group.to_csv('od_matrix.csv')

    group = pd.read_csv('od_matrix.csv')
    nums = list(group['p1'])
    for i in nums:
        group['p1'] = group['p1'].replace(i,province_region[province_id[i]])
    group = group.groupby(['p1','p2']).mean()
    group.to_csv('od_matrix.csv')    

def get_mobility():
    # combine_matrix()
    if not os.path.exists('mobility/'):
        os.mkdir('mobility/')
    df = pd.read_csv('od_matrix.csv')
    date_list = list(df)
    date_list.remove('p1')
    date_list.remove('p2')
    for date in date_list:
        df_date = df[['p1','p2',date]].pivot(index='p1', columns='p2', values=date).fillna(0)
        df_date.to_csv('mobility/'+date+'.csv')



# get_distance()
# get_province_data()
# get_region_data()
get_mobility()