#coding:UTF-8
import requests,datetime,csv,json,copy,time

def check(pro_list,pro_detail):
    if (pro_detail['name'] in pro_list)==False:
        pro_list[pro_detail['name']] = [pro_detail['area'],pro_detail['population'],'']
    return pro_list

def download_data():
    z = 0;y = False
    while y == False:
        try:
            url = 'http://ncov.deepeye.tech/data/data/chinadistrict_level.json'
            r = requests.get(url,timeout=1)
            with open('Tsinghua_district.json','w') as data:
                data.write(r.text)
            y = True
            print('地区数据下载完成')
        except Exception:
            print('10秒后重试')
            time.sleep(10)
            z+=1
            if z==10:print("请求失败");exit(-1)
    z = 0;y = False
    while y == False:
        try:
            url = 'http://ncov.deepeye.tech/data/data/chinaprovince_level.json'
            r = requests.get(url,timeout=1)
            with open('Tsinghua_province.json','w') as data:
                data.write(r.text)
            y = True
            print('省级数据下载完成')
        except Exception:
            print('10秒后重试')
            time.sleep(10)
            z+=1
            if z==10:print("请求失败");exit(-1)

    with open('Tsinghua_province.json') as f:
        data = json.load(f)
        g = open('省级疫情汇总_2.csv','a',newline='')
        gg = open('省级疫情汇总_2.csv','r')
        csv_writer = csv.writer(g)
        haveDate = list(csv.reader(gg))[-1][0]
        datestart = datetime.datetime.strptime(haveDate,'%Y-%m-%d')+datetime.timedelta(days=+1)
        date_index = 0
        if datetime.datetime.strptime(data[0]['time'],'%Y-%m-%d') >= datestart:
            for i in range(len(data)):                             
                if datetime.datetime.strptime(data[i]['time'],'%Y-%m-%d') >= datestart:
                    date_index = i
            print("Need to update ",date_index+1,"-day data")
        else: print("Don't need to update data");exit(0)

        for i in range(date_index+1):
            row = data[date_index-i]
            date = row['time']
            print('更新',date,'省级数据')
            pro_list = {}
            for pro_detail in row['confirm']['province_level']:
                pro_name = pro_detail['name']
                pro_list[pro_name] = [pro_detail['area'],pro_detail['population'],pro_detail['value']]
            for pro_detail in row['suspect']['province_level']:
                pro_name = pro_detail['name']
                pro_list = check(pro_list,pro_detail)
                pro_list[pro_name].append(pro_detail['value'])
            for pro_detail in row['cure']['province_level']:
                pro_name = pro_detail['name']
                pro_list = check(pro_list,pro_detail)
                pro_list[pro_name].append(pro_detail['value'])
            for pro_detail in row['die']['province_level']:
                pro_name = pro_detail['name']
                pro_list = check(pro_list,pro_detail)
                pro_list[pro_name].append(pro_detail['value'])
            for pro_detail in row['currentConfirm']['province_level']:
                pro_name = pro_detail['name']
                pro_list = check(pro_list,pro_detail)
                pro_list[pro_name].append(pro_detail['value'])
            for name in pro_list:
                csv_writer.writerow([date,name,'']+pro_list[name])
    with open('Tsinghua_district.json') as f:
        data = json.load(f)
        g = open('地区疫情汇总_2.csv','a',newline='')
        gg = open('地区疫情汇总_2.csv','r')
        csv_writer = csv.writer(g)
        haveDate = list(csv.reader(gg))[-1][0]
        datestart = datetime.datetime.strptime(haveDate,'%Y-%m-%d')+datetime.timedelta(days=+1)
        date_index = 0
        if datetime.datetime.strptime(data[0]['time'],'%Y-%m-%d') >= datestart:
            for i in range(len(data)):                             
                if datetime.datetime.strptime(data[i]['time'],'%Y-%m-%d') >= datestart:
                    date_index = i
            print("Need to update ",date_index+1,"-day data")
        else: print("Don't need to update data");exit(0)

        for i in range(date_index+1):
            row = data[date_index-i]
            date = row['time']
            print('更新',date,'地区数据')
            dis_list = {}
            for dis_detail in row['confirm']['district_level']:
                dis_name = dis_detail['name']
                dis_list[dis_name] = [dis_detail['area'],dis_detail['population'],dis_detail['value']]
            for dis_detail in row['suspect']['district_level']:
                dis_name = dis_detail['name']
                dis_list = check(dis_list,dis_detail)
                dis_list[dis_name].append(dis_detail['value'])
            for dis_detail in row['cure']['district_level']:
                dis_name = dis_detail['name']
                dis_list = check(dis_list,dis_detail)
                dis_list[dis_name].append(dis_detail['value'])
            for dis_detail in row['die']['district_level']:
                dis_name = dis_detail['name']
                dis_list = check(dis_list,dis_detail)
                dis_list[dis_name].append(dis_detail['value'])
            for dis_detail in row['currentConfirm']['district_level']:
                dis_name = dis_detail['name']
                dis_list = check(dis_list,dis_detail)
                dis_list[dis_name].append(dis_detail['value'])
            for name in dis_list:
                csv_writer.writerow([date,'',name]+dis_list[name])

download_data()
    