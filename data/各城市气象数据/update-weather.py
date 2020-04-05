import json,requests,time,datetime,os,csv

with open('major_city.txt','r',encoding='utf-8') as g:
    citylist = list(g)
with open('天气_id.json') as g:
    data_id = json.load(g)

if os.path.exists('./主要城市平均温度湿度aqi.csv') == False:
    havedate = '2019-12-31'
else:
    with open('./主要城市平均温度湿度aqi.csv') as h:
        havedate = list(csv.reader(h))[-1][0]
datestart = datetime.datetime.strptime(havedate,'%Y-%m-%d')+datetime.timedelta(days=+1)
dateend = datetime.datetime.now()+datetime.timedelta(days=-1)
while datestart < dateend:
    date = datestart.strftime('%Y-%m-%d')
    for city in citylist:
        city_name = city.split('\n')[0]
        city_id = data_id[city_name]
        y = False;z=0
        while y==False:
            url = 'http://api.k780.com/?app=weather.history&weaid='+city_id+'&date='+date+'&appkey=48684&sign=d2c630c7b02b1893eb6797c055857f4f&format=json'
            r = requests.get(url).text
            data = json.loads(r)
            if data['success'] != '0':
                y = True
                print('写入',date,' ',city_name,'数据')
                temp_ave = 0;hum_ave = 0;aqi_ave = 0;n = len(data['result'])
                for detail in data['result']:
                    update_time = detail['uptime']
                    temp = detail['temperature']
                    temp_ave += int(temp[0:-1])/n
                    hum = detail['humidity']
                    hum_ave += int(hum[0:-1])/n
                    aqi = detail['aqi']
                    aqi_ave += int(aqi)/n
                    path_city = './'+city_name+'.csv'
                    if os.path.exists(path_city) == False:
                        with open(path_city,'a',newline='') as f:
                            csv_writer = csv.writer(f)
                            csv_writer.writerow(['日期','温度','湿度','aqi','更新日期'])
                    with open(path_city,'a',newline='') as f:
                        csv_writer = csv.writer(f)
                        csv_writer.writerow([date,temp,hum,aqi,update_time])
                if os.path.exists('./主要城市平均温度湿度aqi.csv') == False:
                    with open('./主要城市平均温度湿度aqi.csv','a',newline='') as f:
                        csv_writer = csv.writer(f)
                        csv_writer.writerow(['日期','城市','温度','湿度','aqi'])
                with open('./主要城市平均温度湿度aqi.csv','a',newline='') as f:
                    csv_writer = csv.writer(f)
                    csv_writer.writerow([date,city_name,temp_ave,hum_ave,aqi_ave])                    
            else:
                print('重新请求')
                time.sleep(3)
                z+=1
                if z==2:print('1h后继续请求');time.sleep(3600)
    datestart+= datetime.timedelta(days=+1)
