# coding:UTF-8
# 文件保存路径 ”./主要城市/迁入迁出指数(迁入迁出比例)/“，各省目录下分表汇总为省级总表
#----------------------------------------------------------------------------------------------------------------------------
import requests
import json
import xlwt,xlrd
import datetime,time
import os
from xlutils.copy import copy

def write_excel_index(province,name,r_in,r_out):                                # 写入数据迁入迁出规模指数
    print("写入"+province+name+"规模指数 ...")
    f = xlwt.Workbook()
    default = set_style('Times New Roman',220,True)
    sheet1 = f.add_sheet('迁入迁出规模指数',cell_overwrite_ok=True)
    row0 = ["日期","迁入规模指数","迁出规模指数"]
    for i in range(len(row0)):
        sheet1.write(0,i,row0[i],default)
    nrows = 1
    datestart = datetime.datetime.strptime('20200101','%Y%m%d')
    for date in r_in['data']['list']:
        date_current = datetime.datetime.strptime(date,'%Y%m%d')
        if datestart<= date_current:
            sheet1.write(nrows,0,date,default)
            sheet1.write(nrows,1,r_in['data']['list'][date],default)
            sheet1.write(nrows,2,r_out['data']['list'][date],default)
            nrows += 1
    target_path = './主要城市/迁入迁出指数/'+province+'/'
    if os.path.exists(target_path) == False:
        os.makedirs(target_path)
    f.save(target_path+name+'.xls')

def write_excel_rank(province,name,r_in_prorank,r_out_prorank,r_in_cityrank,r_out_cityrank,date,r_in_index,r_out_index):
    print("写入 "+date+" "+province+name+"迁入迁出比例 ...")                       # 写入数据迁入迁出比例      
    f = xlwt.Workbook()
    default = set_style('Times New Roman',220,True)
    sheet1 = f.add_sheet(date+'迁入迁出比例',cell_overwrite_ok=True)
    row0 = ["迁入规模指数","迁出规模指数","按省级","迁入比例","迁入指数乘比例","迁出比例","迁出指数乘比例","  ","按市级","  ","迁入比例","迁入指数乘比例","迁出比例","迁出指数乘比例"]
    for i in range(len(row0)):
        sheet1.write(0,i,row0[i],default)
    sheet1.write(1,0,r_in_index,default)
    sheet1.write(1,1,r_out_index,default)

    provincelist_out_prorank = []                                               # 按省份迁入迁出数据
    move_out_prorank = []
    for data_province in r_out_prorank['data']['list']:
        provincelist_out_prorank.append(data_province['province_name'])
        move_out_prorank.append(data_province['value'])
    dict_out_prorank = dict(zip(provincelist_out_prorank,move_out_prorank))
    
    nrows = 1
    for data_province in r_in_prorank['data']['list']:
        province_name = data_province['province_name']
        move_in = data_province['value']
        move_in_index = move_in*r_in_index
        sheet1.write(nrows,2,province_name,default)
        sheet1.write(nrows,3,move_in,default)
        sheet1.write(nrows,4,move_in_index,default)
        if province_name in provincelist_out_prorank:                           # 在迁入数据中查找
            move_out = dict_out_prorank[province_name]
            move_out_index = move_out*r_out_index
            sheet1.write(nrows,5,move_out,default)
            sheet1.write(nrows,6,move_out_index,default)
            del dict_out_prorank[province_name]
        nrows = nrows+1
    if dict_out_prorank != None:
        for province_name in dict_out_prorank:
            move_out = dict_out_prorank[province_name]
            move_out_index = move_out*r_out_index
            sheet1.write(nrows,2,province_name,default)
            sheet1.write(nrows,5,move_out,default)
            sheet1.write(nrows,6,move_out_index,default)
            nrows = nrows+1

    citylist_out_cityrank = []                                                  # 按城市迁入迁出数据
    provincelist_out_cityrank = []
    move_out_cityrank = []
    for data_city in r_out_cityrank['data']['list']:
        citylist_out_cityrank.append(data_city['city_name'])
        provincelist_out_cityrank.append(data_city['province_name'])
        move_out_cityrank.append(data_city['value'])
    citydetails_out_cityrank = list(zip(provincelist_out_cityrank,move_out_cityrank))
    dict_out_cityrank = dict(zip(citylist_out_cityrank,citydetails_out_cityrank))

    nrows = 1
    for data_city in r_in_cityrank['data']['list']:
        city_name = data_city['city_name']
        province_name = data_city['province_name']
        move_in = data_city['value']
        move_in_index = move_in*r_in_index
        sheet1.write(nrows,8,city_name,default)
        sheet1.write(nrows,9,province_name,default)
        sheet1.write(nrows,10,move_in,default)
        sheet1.write(nrows,11,move_in_index,default)
        if city_name in citylist_out_cityrank:                                  # 在迁入数据中查找
            move_out = dict_out_cityrank[city_name][1]
            move_out_index = move_out*r_out_index
            sheet1.write(nrows,12,move_out,default)
            sheet1.write(nrows,13,move_out_index,default)
            del dict_out_cityrank[city_name]
        nrows = nrows+1
    if dict_out_cityrank != None:
        for city_name in dict_out_cityrank:
            province_name = dict_out_cityrank[city_name][0]
            move_out = dict_out_cityrank[city_name][1]
            move_out_index = move_out*r_out_index
            sheet1.write(nrows,8,city_name,default)
            sheet1.write(nrows,9,province_name,default)
            sheet1.write(nrows,12,move_out,default)
            sheet1.write(nrows,13,move_out_index,default)
            nrows = nrows+1

    target_path = './主要城市/迁入迁出比例/按时间序列_地区分表/'+date+'/'+province+'/'
    if os.path.exists(target_path) == False:
        os.makedirs(target_path)
    f.save(target_path+name+'.xls')

def set_style(name,height,bold=False):                                          # 定义 Excel 属性
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

def extract_json_data(r):                                                       # extract json data
    start1 = '('
    end1 = ')'
    s = r.text.find(start1)
    e = r.text.find(end1)
    sub_str = r.text[s+1:e]
    return json.loads(sub_str)

def download_data():
    dateend = datetime.datetime.now()+datetime.timedelta(days=-2)
    endDate = datetime.datetime.strftime(dateend,'%Y%m%d')
    path_have = './主要城市/迁入迁出比例/按地区_时间总表/上海/'
    haveDate = '20191231'
    for root,dirs,files in os.walk(path_have):
        for name in files:
            if name.split('.')[1]=='xls':
                haveDate = name.split('.')[0].split('_')[1]
    datehave = datetime.datetime.strptime(haveDate,'%Y%m%d')

    with open('./id.json') as f:
        data_id = json.load(f)
    with open('majorcity.txt','r',encoding='UTF-8') as f:
        majorcity = list(f)
    
    headers = {'Connection':'close'}
    for province_id in data_id['0']:
        province_name = data_id['0'][province_id]                               # 各省迁入迁出规模指数
        url_in_province = 'http://huiyan.baidu.com/migration/historycurve.jsonp?dt=province&id='+province_id+'&type=move_in&startDate=20200101&endDate='+endDate
        url_out_province = 'http://huiyan.baidu.com/migration/historycurve.jsonp?dt=province&id='+province_id+'&type=move_out&startDate=20200101&endDate='+endDate
        y,z = 0,0
        while y == 0:
            try:
                r_in_province = extract_json_data(requests.get(url_in_province,stream=True,headers=headers,timeout=1))
                r_out_province = extract_json_data(requests.get(url_out_province,stream=True,headers=headers,timeout=1))
                y = 1
            except Exception:
                print("10秒后重新请求")
                time.sleep(10)
                z+=1
                if z == 10: print("请求失败");break
        write_excel_index(province_name,'省级总表',r_in_province,r_out_province)
        datestart = datehave
        while datestart < dateend:                                             # 各省迁入迁出比例
            datestart+=datetime.timedelta(days=+1)
            date = datetime.datetime.strftime(datestart,'%Y%m%d')
            if date in r_in_province['data']['list']:
                province_in_index = r_in_province['data']['list'][date]
                province_out_index = r_out_province['data']['list'][date]
            url_in_province_prorank = 'http://huiyan.baidu.com/migration/provincerank.jsonp?dt=province&id='+province_id+'&type=move_in&date='+date
            url_out_province_prorank = 'http://huiyan.baidu.com/migration/provincerank.jsonp?dt=province&id='+province_id+'&type=move_out&date='+date
            url_in_province_cityrank = 'http://huiyan.baidu.com/migration/cityrank.jsonp?dt=province&id='+province_id+'&type=move_in&date='+date
            url_out_province_cityrank = 'http://huiyan.baidu.com/migration/cityrank.jsonp?dt=province&id='+province_id+'&type=move_out&date='+date
            y,z = 0,0
            while y == 0:
                try:
                    r_in_province_prorank = extract_json_data(requests.get(url_in_province_prorank,stream=True,headers=headers,timeout=1))
                    r_out_province_prorank = extract_json_data(requests.get(url_out_province_prorank,stream=True,headers=headers,timeout=1))
                    r_in_province_cityrank = extract_json_data(requests.get(url_in_province_cityrank,stream=True,headers=headers,timeout=1))
                    r_out_province_cityrank = extract_json_data(requests.get(url_out_province_cityrank,stream=True,headers=headers,timeout=1))
                    y = 1
                except Exception:
                    print("10秒后重新请求")
                    time.sleep(10)
                    z+=1
                    if z == 10: print("请求失败");break
            write_excel_rank(province_name,'省级总表',r_in_province_prorank,r_out_province_prorank,r_in_province_cityrank,r_out_province_cityrank,date,province_in_index,province_out_index)


        for city_id in data_id['0,'+province_id]:                               # 各市迁入迁出规模指数
            city_name = data_id['0,'+province_id][city_id]
            url_in_city = 'http://huiyan.baidu.com/migration/historycurve.jsonp?dt=city&id='+city_id+'&type=move_in&startDate=20200101&endDate='+endDate
            url_out_city = 'http://huiyan.baidu.com/migration/historycurve.jsonp?dt=city&id='+city_id+'&type=move_out&startDate=20200101&endDate='+endDate
            y,z = 0,0
            while y == 0:
                try:
                    r_in_city = extract_json_data(requests.get(url_in_city,stream=True,headers=headers,timeout=1))
                    r_out_city = extract_json_data(requests.get(url_out_city,stream=True,headers=headers,timeout=1))
                    y = 1
                except Exception:
                    print("10秒后重新请求")
                    time.sleep(10)
                    z+=1
                    if z == 10: print("请求失败");break
            if len(r_in_city['data']['list']) != 0:    
                write_excel_index(province_name,city_name,r_in_city,r_out_city)
                if city_name+'\n' in majorcity:
                    datestart = datehave
                    while datestart < dateend:                                         # 各市迁入迁出比例
                        datestart+=datetime.timedelta(days=+1)
                        date = datetime.datetime.strftime(datestart,'%Y%m%d')
                        if date in r_in_city['data']['list']:
                            city_in_index = r_in_city['data']['list'][date]
                            city_out_index = r_out_city['data']['list'][date]
                        url_in_city_prorank = 'http://huiyan.baidu.com/migration/provincerank.jsonp?dt=city&id='+city_id+'&type=move_in&date='+date
                        url_out_city_prorank = 'http://huiyan.baidu.com/migration/provincerank.jsonp?dt=city&id='+city_id+'&type=move_out&date='+date
                        url_in_city_cityrank = 'http://huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id='+city_id+'&type=move_in&date='+date
                        url_out_city_cityrank = 'http://huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id='+city_id+'&type=move_out&date='+date
                        y,z = 0,0
                        while y == 0:
                            try:
                                r_in_city_prorank = extract_json_data(requests.get(url_in_city_prorank,stream=True,headers=headers,timeout=1))
                                r_out_city_prorank = extract_json_data(requests.get(url_out_city_prorank,stream=True,headers=headers,timeout=1))
                                r_in_city_cityrank = extract_json_data(requests.get(url_in_city_cityrank,stream=True,headers=headers,timeout=1))
                                r_out_city_cityrank = extract_json_data(requests.get(url_out_city_cityrank,stream=True,headers=headers,timeout=1))
                                y = 1
                            except Exception:
                                print("10秒后重新请求")
                                time.sleep(10)
                                z+=1
                                if z == 10: print("请求失败");break
                        write_excel_rank(province_name,city_name,r_in_city_prorank,r_out_city_prorank,r_in_city_cityrank,r_out_city_cityrank,date,city_in_index,city_out_index)
    print("数据下载完成")

def compact():                                                                  # 部分整合为面板数据
    default = set_style('Times New Roman',220,True)                             # 整合规模指数
    with open('./id.json') as f:
        data_id = json.load(f)

    provincelist_index = []
    citylist_index = []
    for province_id in data_id['0']:
        province_name = data_id['0'][province_id]
        path = './主要城市/迁入迁出指数/'+province_name+'/'
        if os.path.exists(path+'省级总表.xls')==True:
            data_pro = xlrd.open_workbook(path+'省级总表.xls')
            table_pro = data_pro.sheets()[0]
            nrows_pro = table_pro.nrows
            prolist = []
            print("添加 ",path+'省级总表.xls')
            for i in range(1,nrows_pro):
                province_index = table_pro.row_values(i,start_colx=0,end_colx=None)
                province_index.insert(1,"  ")
                province_index.insert(2,province_name)
                prolist.append(province_index)
            provincelist_index.append(prolist)

        for city_id in data_id['0,'+province_id]:
            city_name = data_id['0,'+province_id][city_id]
            if os.path.exists(path+city_name+'.xls')==True:
                data_city = xlrd.open_workbook(path+city_name+'.xls')
                table_city = data_city.sheets()[0]
                nrows_city = table_city.nrows
                citylist = []
                print("添加 ",path+city_name+'.xls')
                for i in range(1,nrows_city):
                    city_index = table_city.row_values(i,start_colx=0,end_colx=None)
                    city_index.insert(1,city_name)
                    city_index.insert(2,province_name)
                    citylist.append(city_index)
                citylist_index.append(citylist)
        if province_name in ['北京','天津','上海','重庆','香港特别行政区','澳门特别行政区']:
            data_city = xlrd.open_workbook(path+'省级总表.xls')
            table_city = data_city.sheets()[0]
            nrows_city = table_city.nrows
            citylist = []
            print("添加 ",path+'省级总表.xls')
            for i in range(1,nrows_city):
                city_index = table_city.row_values(i,start_colx=0,end_colx=None)
                city_index.insert(1,province_name)
                city_index.insert(2,province_name)
                citylist.append(city_index)
            citylist_index.append(citylist)

    f_pro_index = xlwt.Workbook()
    sheet_pro_index = f_pro_index.add_sheet('全国省级规模指数',cell_overwrite_ok=True)
    row0 = ["日期","  ","省级","迁入规模指数","迁出规模指数"]
    for i in range(len(row0)):
        sheet_pro_index.write(0,i,row0[i],default)
    num_pro_index = len(provincelist_index)
    for i in range(len(provincelist_index[0])):
        for j in range(num_pro_index):
            for k in range(len(provincelist_index[j][i])):
                sheet_pro_index.write(i*num_pro_index+j+1,k,provincelist_index[j][i][k],default)
    f_pro_index.save('./主要城市/迁入迁出指数/省级_全国总表.xls')

    f_city_index = xlwt.Workbook()
    sheet_city_index = f_city_index.add_sheet('全国市级规模指数',cell_overwrite_ok=True)
    row0 = ["日期","市级","省级","迁入规模指数","迁出规模指数"]
    for i in range(len(row0)):
        sheet_city_index.write(0,i,row0[i],default)
    num_city_index = len(citylist_index)
    for j in range(num_city_index):
        for i in range(len(citylist_index[j])):
            for k in range(len(citylist_index[j][i])):
                sheet_city_index.write(i*num_city_index+j+1,k,citylist_index[j][i][k],default)
    f_city_index.save('./主要城市/迁入迁出指数/市级_全国总表.xls')

    dateend = datetime.datetime.now()+datetime.timedelta(days=-2)
    haveDate = '20191231'
    path_have = './主要城市/迁入迁出比例/按地区_时间总表/上海/'
    haveDate = '20191231'
    for root,dirs,files in os.walk(path_have):
        for name in files:
            if name.split('.')[1]=='xls':
                haveDate = name.split('.')[0].split('_')[1]
    datehave = datetime.datetime.strptime(haveDate,'%Y%m%d')

    for province_id in data_id['0']:
        prolist = []                                                            # 整合迁入迁出比例
        province_name = data_id['0'][province_id]
        datestart = datehave
        while datestart < dateend:                                              # 各省迁入迁出比例
            datestart+=datetime.timedelta(days=+1)
            date = datetime.datetime.strftime(datestart,'%Y%m%d')
            path = './主要城市/迁入迁出比例/按时间序列_地区分表/'+date+'/'+province_name+'/'
            if os.path.exists(path+'省级总表.xls')==True:
                data_pro = xlrd.open_workbook(path+'省级总表.xls')
                table_pro = data_pro.sheets()[0]
                nrows_pro = table_pro.nrows
                date_had = date
                print("添加 ",path+'省级总表.xls')
                for i in range(1,nrows_pro):
                    province_rank = table_pro.row_values(i,start_colx=0,end_colx=None)
                    province_rank.insert(0,date)
                    province_rank.insert(1,"  ")
                    province_rank.insert(2,province_name)
                    prolist.append(province_rank)
        if len(prolist) != 0:
            path_rank = './主要城市/迁入迁出比例/按地区_时间总表/'+province_name+'/'
            if os.path.exists(path_rank) == False:
                os.makedirs(path_rank)
            data_all = xlrd.open_workbook(path_rank+'省级总表_'+haveDate+'.xls')
            excel_all = copy(wb=data_all)
            excel_table_all = excel_all.get_sheet(0)
            table_all = data_all.sheets()[0]
            nrows = table_all.nrows
            for i in range(len(prolist)):
                for k in range(len(prolist[i])):
                    excel_table_all.write(nrows,k,prolist[i][k],default)
                nrows = nrows+1
            excel_all.save(path_rank+'省级总表_'+date_had+'.xls')
            os.remove(path_rank+'省级总表_'+haveDate+'.xls')
        del prolist

        for city_id in data_id['0,'+province_id]:
            citylist = []
            city_name = data_id['0,'+province_id][city_id]
            datestart = datehave
            while datestart <= dateend:                                             # 各市迁入迁出比例
                datestart+=datetime.timedelta(days=+1)
                date = datetime.datetime.strftime(datestart,'%Y%m%d')
                path = './主要城市/迁入迁出比例/按时间序列_地区分表/'+date+'/'+province_name+'/'
                if os.path.exists(path+city_name+'.xls')==True:
                    data_city = xlrd.open_workbook(path+city_name+'.xls')
                    table_city = data_city.sheets()[0]
                    nrows_city = table_city.nrows
                    date_had = date
                    print("添加 ",path+city_name+'.xls')
                    for i in range(1,nrows_city):
                        city_rank = table_city.row_values(i,start_colx=0,end_colx=None)
                        city_rank.insert(0,date)
                        city_rank.insert(1,city_name)
                        city_rank.insert(2,province_name)
                        citylist.append(city_rank)
            if len(citylist) != 0:
                path_rank = './主要城市/迁入迁出比例/按地区_时间总表/'+province_name+'/'
                data_all = xlrd.open_workbook(path_rank+city_name+'_'+haveDate+'.xls')
                excel_all = copy(wb=data_all)
                excel_table_all = excel_all.get_sheet(0)
                table_all = data_all.sheets()[0]
                nrows = table_all.nrows
                for i in range(len(citylist)):
                    for k in range(len(citylist[i])):
                        excel_table_all.write(nrows,k,citylist[i][k],default)
                    nrows = nrows+1
                excel_all.save(path_rank+city_name+'_'+date_had+'.xls')
                os.remove(path_rank+city_name+'_'+haveDate+'.xls')
            del citylist

download_data()
compact()