import pandas as pd
import os,requests,json,time,datetime

def get_mobility():
    with open('./id.json') as f:
        data_id = json.load(f)
    df_nums = pd.read_csv('./迁移规模指数/省级总表.csv')
    nums = {}
    for index in df_nums.index:
        row = df_nums.loc[index].values
        nums[str(row[0])+row[2]] = row[4]

    date = '20201001'
    start_date = datetime.datetime.strptime(date,'%Y%m%d')
    datehave = datetime.datetime.today() + datetime.timedelta(days=-1)
    while start_date < datehave:
        NE = True
        date = datetime.datetime.strftime(start_date,'%Y%m%d')
        data_date = pd.DataFrame(columns=[])
        i = 0
        for province_id in data_id['0']:
            province_name = data_id['0'][province_id]
            province_num = nums[date+province_name]
            url = 'https://huiyan.baidu.com/migration/provincerank.jsonp?dt=province&id={}&type=move_out&date={}'.format(province_id,date)
            z = 0
            while True:
                try:
                    r = requests.get(url,timeout=1).text
                    break
                except Exception:
                    z += 1
                    if z >= 10: exit(-1)
                    print('10秒后重新请求')
                    time.sleep(10)
            r_json = json.loads(r[4:-1])
            if r_json['errno'] == 0:
                df = pd.DataFrame(r_json['data']['list'])
                df = df.set_index('province_name')
                if province_name in ['北京','重庆','上海','天津']:
                    province_name = province_name + '市'
                df['value'] = df['value']/100 * province_num
                df.columns = [province_name]
                data_date = pd.concat([data_date,df],axis=1)
            else:
                NE = False
                break
        if NE:
            if not os.path.exists('./mobility/'):
                os.mkdir('mobility/')
            data_date.T.to_csv('./mobility/'+date+'.csv')
        start_date += datetime.timedelta(days=1)

def get_distance():
    with open('./China_loc.json','r') as f:
        location = json.load(f)

    df = pd.DataFrame(location)
    print(df)
    eixt(0)

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

    
get_mobility()




