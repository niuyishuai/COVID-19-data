# coding:UTF-8
import requests,json,os,datetime,time
import xlwt,xlrd
from xlutils.copy import copy

# 更新数据至总表分表（可以从头更新）
def details(level0='province'):
    filepath = './details/'+level0+'.xls'
    datestart = latestday(days_had(filepath,level0))
    with open('./details/details.json') as f:
        req_data = json.load(f)[level0]
    default = set_style('Times New Roman',220,True)
    date_index = 0
    if datetime.datetime.strptime(req_data[0]['Time'],'%Y-%m-%d') >= datestart:
        for i in range(len(req_data)):                             
            if datetime.datetime.strptime(req_data[i]['Time'],'%Y-%m-%d') >= datestart:
                date_index = i
        print("Need to update ",date_index+1,"-day data")
    else: print("Don't need to update data");exit(0)

    for i in range(date_index+1):                              
        index = date_index-i                                   # 从起始日期开始更新
        date = req_data[index]['Time']
        f = xlwt.Workbook()
        sheet1 = f.add_sheet(level0+'Details',cell_overwrite_ok=True)
        if level0 == 'city':                                   # 输入标题
            row0 = ["城市","省份","确诊","死亡","治愈","疑似"]
            level = 'City'
        else:
            row0 = ["  ","省份","确诊","死亡","治愈","疑似"]
            level = 'Province'
        for i in range(0,len(row0)):
            sheet1.write(0,i,row0[i],set_style('Times New Roman',220,True))

        i = 0
        for req_dict in req_data[index][level+'Detail']:       # 写入分表
            if level == 'City':
                city_name = req_dict['City']
                sheet1.write(i+1,0,city_name,set_style('Times New Roman',220,True))
            province_name = req_dict['Province']
            confirmed = req_dict['Confirmed']
            dead = req_dict['Dead']
            cured = req_dict['Cured']
            if 'Obse' in req_dict:
                obse = req_dict['Obse']
                sheet1.write(i+1,5,obse,set_style('Times New Roman',220,True))
            sheet1.write(i+1,1,province_name,set_style('Times New Roman',220,True))
            sheet1.write(i+1,2,confirmed,set_style('Times New Roman',220,True))
            sheet1.write(i+1,3,dead,set_style('Times New Roman',220,True))
            sheet1.write(i+1,4,cured,set_style('Times New Roman',220,True))
            i = i+1
        target_path = './details/'+level+'/'                   # 判断生成路径
        if os.path.exists(target_path) == False:
            os.makedirs(target_path)
        f.save(target_path+date+'.xls')

        print(date,' writting ...')
        data_all = xlrd.open_workbook(filepath)                # 写入总表
        excel_all = copy(wb=data_all)
        excel_table_all = excel_all.get_sheet(0)
        table_all = data_all.sheets()[0]
        nrows = table_all.nrows
        for req_dict in req_data[index][level+'Detail']:
            if level == 'City':
                city_name = req_dict[level]
                excel_table_all.write(nrows,1,city_name,default)
            province_name = req_dict['Province']
            confirmed = req_dict['Confirmed']
            dead = req_dict['Dead']
            cured = req_dict['Cured']
            if 'Obse' in req_dict:
                obse = req_dict['Obse']
                excel_table_all.write(nrows,6,obse,default)
            excel_table_all.write(nrows,0,date,default)
            excel_table_all.write(nrows,2,province_name,default)
            excel_table_all.write(nrows,3,confirmed,default)
            excel_table_all.write(nrows,4,dead,default)
            excel_table_all.write(nrows,5,cured,default)
            nrows = nrows+1
        excel_all.save(filepath)
        print(date,' done')

def latestday(datelist):                                       # 输出日期列表的下一天
    latest_day = datetime.datetime.strptime('2020-01-01','%Y-%m-%d')
    for date in datelist:
        current_day = datetime.datetime.strptime(date,'%Y-%m-%d')
        current_day += datetime.timedelta(days=+1)
        if latest_day<current_day:
            latest_day = current_day
    return latest_day

def days_had(filepath,level0):
    if os.path.exists(filepath) == False:                      # 检验总表存在
        if os.path.exists('./details/') == False:
            os.makedirs('./details/')
        datelist = []
        f = xlwt.Workbook()                                    # 新建总表并输入标题
        sheet1 = f.add_sheet(level0+'Details',cell_overwrite_ok=True)
        if level0 == 'city':
            row0 = ["日期","城市","省份","确诊","死亡","治愈","疑似"]
        else:
            row0 = ["日期","  ","省份","确诊","死亡","治愈","疑似"]
        for i in range(0,len(row0)):
            sheet1.write(0,i,row0[i],set_style('Times New Roman',220,True))
        f.save(filepath)
    else:                                                      # 输出总表中日期列表
        data = xlrd.open_workbook(filepath)
        table = data.sheets()[0]
        datelist = table.col_values(0,start_rowx=1,end_rowx=None)
    return datelist

def set_style(name,height,bold=False):                         # 定义 Excel 属性
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

def update_data():                                             # 更新数据
    print("connecting to API ...")
    url = 'http://ncov.nosensor.com:8080/api/'                 # 下载 API 数据并保存
    headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    y = False;z = 0
    while y == False:
        try:
            r = requests.get(url,headers,stream = True,timeout = 1)
            y = True
        except Exception:
            print('10秒后重试')
            time.sleep(10)
            z += 1
            if z == 10:print('请求失败');exit(-1)
    with open('./details/details.json','w') as f:
        f.write(r.text)
    for level0 in ['city','province']:
        details(level0)

update_data()
