# coding:UTF-8
import requests,json,os,datetime,time
import xlwt,xlrd
from xlutils.copy import copy

# 更新数据至总表分表（可以从头更新）
def migration(level='city',type='move_out',date='20200101'):
    url = 'http://huiyan.baidu.com/migration/'+level+'rank.jsonp?dt=country&id=0&type='+type+'&date='+date+'&callback=jsonp_1580737583074_8938529'
    y = False;z = 0
    while y == False:
        try:
            r = requests.get(url)
            y = True
        except Exception:
            print('10秒后重试')
            time.sleep(10)
            z += 1
            if z==10:print('请求失败');exit(0)
    req_data = extract_json_data(r)                            # 调用API并转化为 json 数据

    default = set_style('Times New Roman',220,True)
    f = xlwt.Workbook()                                        # 写入分表
    sheet1 = f.add_sheet(type,cell_overwrite_ok=True)
    if level == 'city':                                        # 输入标题
        row0 = ["城市","省份","比例"]
    else:
        row0 = ["  ","省份","比例"]
    for i in range(0,len(row0)):
        sheet1.write(0,i,row0[i],default)

    i = 0                                                      # 写入数据
    for req_dict in req_data['data']['list']:
        if level == 'city':
            city_name = req_dict['city_name']
            sheet1.write(i+1,0,city_name,default)
        province_name = req_dict['province_name']
        value = req_dict['value']
        sheet1.write(i+1,1,province_name,default)
        sheet1.write(i+1,2,value,default)
        i = i+1
    
    target_path = './migration/'+level+'/'+type+'/'            # 判断生成路径
    if os.path.exists(target_path) == False:
        os.makedirs(target_path)
    f.save(target_path+date+'.xls')

    data_all = xlrd.open_workbook('./migration/'+level+'.xls') # 写入总表
    excel_all = copy(wb=data_all)
    excel_table_all = excel_all.get_sheet(0)
    table_all = data_all.sheets()[0]
    nrows = table_all.nrows
    if type == 'move_in':                                      # 写入迁入数据
        for req_dict in req_data['data']['list']:
            if level == 'city':
                city_name = req_dict['city_name']
                excel_table_all.write(nrows,1,city_name,default)
            province_name = req_dict['province_name']
            value = req_dict['value']
            excel_table_all.write(nrows,0,date,default)
            excel_table_all.write(nrows,2,province_name,default)
            excel_table_all.write(nrows,3,value,default)
            nrows = nrows+1
        excel_all.save('./migration/'+level+'.xls')
        print(type,' done')
    else:                                                      # 迁出数据按城市查重写入
        datelist_before = table_all.col_values(0,start_rowx = 1,end_rowx = None)
        if date in datelist_before:                            # 查找对应日期
            nrows_before = datelist_before.index(date)
            if level == 'city':
                citylist_all = table_all.col_values(1,start_rowx = nrows_before+1,end_rowx = None)
                for req_dict in req_data['data']['list']:
                    if req_dict['city_name'] in citylist_all:  # 查找城市名，输入对应行
                        s = citylist_all.index(req_dict['city_name'])
                        excel_table_all.write(nrows_before+1+s,4,req_dict['value'],default)
                    else:                                      # 不重复，写入新一行
                        city_name = req_dict['city_name']
                        excel_table_all.write(nrows,1,city_name,default)
                        province_name = req_dict['province_name']
                        value = req_dict['value']
                        excel_table_all.write(nrows,0,date,default)
                        excel_table_all.write(nrows,2,province_name,default)
                        excel_table_all.write(nrows,4,value,default)
                        nrows = nrows+1
            else:
                provincelist_all = table_all.col_values(2,start_rowx = nrows_before+1,end_rowx = None)
                for req_dict in req_data['data']['list']:      # 查找省份名，输入对应行
                    if req_dict['province_name'] in provincelist_all:
                        s = provincelist_all.index(req_dict['province_name'])
                        excel_table_all.write(nrows_before+1+s,4,req_dict['value'],default)
                    else:
                        province_name = req_dict['province_name']
                        value = req_dict['value']
                        excel_table_all.write(nrows,0,date,default)
                        excel_table_all.write(nrows,2,province_name,default)
                        excel_table_all.write(nrows,4,value,default)
                        nrows = nrows+1
            excel_all.save('./migration/'+level+'.xls')
            print(type,' done')
        else: print(level," Complete")

def set_style(name,height,bold=False):                         # 定义 Excel 属性
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

def extract_json_data(r):                                      # jsonp_data to json_data
    start1 = '('
    end1 = ')'
    s = r.text.find(start1)
    e = r.text.find(end1)
    sub_str = r.text[s+1:e]
    return json.loads(sub_str)

def latestday(datelist):                                       # 查找日期列表的下一天
    latest_day = datetime.datetime.strptime('20200101','%Y%m%d')
    for date in datelist:
        current_day = datetime.datetime.strptime(date,'%Y%m%d')
        current_day += datetime.timedelta(days=+1)
        if latest_day<current_day:
            latest_day = current_day
    return latest_day

def days_had(filepath,level):                                  # 收集当前已有数据日期列表
    if os.path.exists(filepath) == False:                      # 查找总表存在
        if os.path.exists('./migration/') == False:
            os.makedirs('./migration/')
        datelist = []
        f = xlwt.Workbook()                                    # 新建总表，输入标题
        sheet1 = f.add_sheet(level+'migrations',cell_overwrite_ok=True)
        if level == 'city':
            row0 = ["日期","城市","省份","迁入比例","迁出比例"]
        else:
            row0 = ["日期","  ","省份","迁入比例","迁出比例"]
        for i in range(0,len(row0)):
            sheet1.write(0,i,row0[i],set_style('Times New Roman',220,True))
        f.save(filepath)
    else:                                                      # 输出总表中日期列表
        data = xlrd.open_workbook(filepath)
        table = data.sheets()[0]
        datelist = table.col_values(0,start_rowx=1,end_rowx=None)
    return datelist

def update_data():                                             # 更新数据
    for level in ['city','province']:
        dateend = datetime.datetime.now()
        filepath = './migration/'+level+'.xls'
        datestart = latestday(days_had(filepath,level))
        while datestart < dateend:                             # 更新至当前日期
            date = datestart.strftime('%Y%m%d')
            print(date,"    ",level,' collecting')
            for type in ['move_in','move_out']:
                migration(level,type,date)
            datestart+= datetime.timedelta(days=+1)
        
update_data()