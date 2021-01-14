#coding:UTF-8
import requests,datetime,csv,json,copy,time

def get_int(a_str):
    if (a_str == '')or(a_str == '0')or(a_str=='\u3000'):
        a_int = 0
    else: 
        a_int = int(a_str)
    return a_int

def get_str(a_int):
    if type(a_int) == str:
        a_int = get_int(a_int)
    if a_int == 0:
        a_str = ''
    else: a_str = str(a_int)
    return a_str

def download_data():
    # z = 0;y = False
    # while y == False:
    #     try:
    #         url = 'https://vis.ucloud365.com/ncov/data/map.csv'
    #         headers = {
    #             'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
    #         }
    #         r = requests.get(url,headers=headers,timeout=1)
    #         with open('map.csv','w') as data:
    #             data.write(r.text)
    #         y = True
    #     except Exception:
    #         print('10秒后重试')
    #         time.sleep(10)
    #         z+=1
    #         if z==10:print("请求失败");exit(-1)

    dictlist = {}

    with open('map.csv','r',encoding='utf-8') as f:
        f_csv = csv.reader(f)
        datelist = ['1月10日']
        date_last = '1月10日'
        N_add = 0
        for row in f_csv:
            if row[1] != '类别':
                date = row[0]
                if date != date_last:
                    dictlist[date] = copy.deepcopy(dictlist[date_last])
                    for level in dictlist[date]:
                        for province in dictlist[date][level]:
                            for city in dictlist[date][level][province]:
                                for i in range(3):
                                    dictlist[date][level][province][city][i] = ''
                    datelist.append(date)
                if date in dictlist:
                    if (row[1] in dictlist[date])&(row[1]!='国家级'):
                        if row[2] in dictlist[date][row[1]]:
                            if row[3] in dictlist[date][row[1]][row[2]]:
                                details_last = dictlist[date][row[1]][row[2]][row[3]]
                                confirm_add = get_str(get_int(details_last[3])+get_int(row[4]))
                                dead_add = get_str(get_int(details_last[4])+get_int(row[6]))
                                cured_add = get_str(get_int(details_last[5])+get_int(row[5]))
                                dictlist[date][row[1]][row[2]][row[3]] = [get_str(row[4]),get_str(row[6]),get_str(row[5]),confirm_add,dead_add,cured_add]
                            else:
                                dictlist[date][row[1]][row[2]][row[3]] = [get_str(row[4]),get_str(row[6]),get_str(row[5]),get_str(row[4]),get_str(row[6]),get_str(row[5])]
                        else:
                            dictlist[date][row[1]][row[2]] = {row[3]:[get_str(row[4]),get_str(row[6]),get_str(row[5]),get_str(row[4]),get_str(row[6]),get_str(row[5])]}
                    elif (row[1] in dictlist[date]) == False:
                        dictlist[date][row[1]] = {row[2]:{row[3]:[get_str(row[4]),get_str(row[6]),get_str(row[5]),get_str(row[4]),get_str(row[6]),get_str(row[5])]}}
                    if (row[1]=='省级')&(date!='1月10日'):
                        dictlist[date]['国家级'][''][''][0] = get_str(get_int(dictlist[date]['国家级'][''][''][0])+get_int(row[4]))
                        dictlist[date]['国家级'][''][''][1] = get_str(get_int(dictlist[date]['国家级'][''][''][1])+get_int(row[6]))
                        dictlist[date]['国家级'][''][''][2] = get_str(get_int(dictlist[date]['国家级'][''][''][2])+get_int(row[5]))
                        dictlist[date]['国家级'][''][''][3] = get_str(get_int(dictlist[date]['国家级'][''][''][3])+get_int(row[4]))
                        dictlist[date]['国家级'][''][''][4] = get_str(get_int(dictlist[date]['国家级'][''][''][4])+get_int(row[6]))
                        dictlist[date]['国家级'][''][''][5] = get_str(get_int(dictlist[date]['国家级'][''][''][5])+get_int(row[5]))
                else:
                    dictlist[date] = {row[1]:{row[2]:{row[3]:[get_str(row[4]),get_str(row[6]),get_str(row[5]),get_str(row[4]),get_str(row[6]),get_str(row[5])]}}}
                if row[1] == '':del dictlist[date][row[1]]
                date_last = date
        with open('map.json','w') as f:
            f.write(json.dumps(dictlist))

    with open('map.json') as f:
        data_json = json.load(f)

    with open('疫情新增_汇总.csv','w',newline = '') as h:
        csv_writer = csv.writer(h)
        csv_writer.writerow(['日期','类别','省份','城市','新增确诊','新增死亡','新增治愈','累计确诊','累计死亡','累计治愈'])
        for date in data_json:
            for level in data_json[date]:
                for province in data_json[date][level]:
                    for city in data_json[date][level][province]:
                        csv_writer.writerow([date,level,province,city]+data_json[date][level][province][city])

download_data()
    