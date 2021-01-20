# 中国迁移数据及少部分国外数据

## 百度迁移数据（选取部分主要城市`majorcity.txt`），截止2020.03.09，全部数据详见服务器。脚本`update-major.py`

## 部分全球航班数据（主要集中北美），`opensky_flight`，数据文件过大，详见服务器

## 谷歌人口流动性报告，详见服务器

## Citymapper_Mobility_Index
- 时间：2020/1/20香港（3/1所有）至今
- 涉及城市：39个国外主要城市（含香港）
- 指标：
    -% of city moving compared to usual
- 基于Citymapper app， public transport users and also use us for walking, cycling, and some micromobility and cabs. We are not used for driving. .
- 网址：https://citymapper.com/CMI

## Facebook Movement Range（见服务器）
- 时间：2020/3/1至今
- 指标：
    - ds: Date stamp for movement range data row in YYYY-MM-DD form
    - country: Three-character ISO-3166 country code
    - polygon_source: Source of region polygon, either “FIPS” for U.S. data or “GADM” for global data
    - polygon_id: Unique identifier for region polygon, either numeric string for U.S. FIPS codes or alphanumeric string for GADM regions
    - polygon_name: Region name
    - all_day_bing_tiles_visited_relative_change: Positive or negative change in movement relative to baseline
    - all_day_ratio_single_tile_users: Positive proportion of users staying put within a single location
    - baseline_name: When baseline movement was calculated pre-COVID-19
    - baseline_type: How baseline movement was calculated pre-COVID-19
- 网址：https://data.humdata.org/dataset/movement-range-maps

## state
- 时间：01/01/2020-12/31/2020
- 指标：美国各州流动性，疫情带来的经济影响和易感人群比例等数据
- 网址：https://data.covid.umd.edu/


    - 社会疏远指数*:	从 0~100 的整数表示居民和访客练习社会疏远的程度。"0"表示社区没有社会疏远，而"100"表示所有居民都待在家里，没有访客进入县城。请参阅"方法"页面。由 MTI计算。
    - % 待在家里:	留在家中的居民百分比（即，没有非家庭旅行结束一英里远的家）。由 MTI 计算。
    - 行程/人员:	                每人每天平均旅行次数。由 MTI 计算。
    - 县外旅行百分比:	跨越县边界的所有行程的百分比。由 MTI 计算。
    - 州外旅行百分比*:	跨越州边界的所有行程的百分比。由 MTI 计算。
    - 里程/人:	                每人每天以各种模式（汽车、火车、公共汽车、飞机、自行车、步行等）旅行的平均人英里数。由 MTI 计算。
    - 工作旅行/人员:	每人每天的工作次数（其中"工作旅行"定义为从工作地点去或回家）。由 MTI 计算。
    - 非工作旅行/人员:	每人每天的非工作旅行次数。有关行程目的的其他信息（杂货店、公园、餐厅等）可用，但目前未显示在平台上。由 MTI 计算。
    - 传输模式共享:	铁路和公交交通模式所占份额的百分比。来源：来自ACS的基线传输模式共享;MTI 目前正在根据移动数据使用动态传输模式共享来更新此指标。

    - 新 COVID 案例:	COVID-19每日新病例数。资料来源：JHU COVID-19数据存储库。
    - 新病例/1000人*:	COVID-19 每日每 1000 人新病例数（三天移动平均数）。由MTI基于JHU存储库计算。
    - 活动病例/1000人:	每 1000 人有活动 COVID-19 例数。由 MTI 计算。
    - 导入的 COVID 案例*:	来自州/县的传染病患者每天的对外旅行次数。由 MTI 计算。
    - COVID 曝光/1000 人:	每1000人已经接触冠状病毒的居民人数。由 MTI 计算。
    - 天： 减少 Covid 病例:	COVID-19 病例减少的天数。由 MTI 基于每周新每日病例模式计算。
    - 天数减少 ILI 病例*:	流感样疾病趋势呈下降趋势的天数。由MTI使用CDC每周美国流感监测报告计算。
    - 测试容量差距*:	能够根据世界卫生组织推荐的阳性检测率代理提供足够的检测。高阳性测试率表明没有足够的测试和测试能力差距。资料来源：COVID跟踪项目。
    - 测试完成/1000 人:	每 1000 人已完成 COVID-19 测试的数量。资料来源：COVID跟踪项目。
    - 接触追踪工作者/1000 人*:	每10万人接触追踪工作者人数。资料来源：国家公共卫生部门NPR调查。
    - 医院病床利用率百分比*:	医院病床占病人的百分比。由 MTI 使用ESRI 计算：美国医院病床仪表板和IMHE COVID-19 预测
    - % ICU 利用率*:	% ICU 联合占用 COVID-19 患者。由MTI使用ESRI计算：美国医院病床仪表板，COVID跟踪项目和 IMHE COVID-19预测。
    - 医院病床/1000人:	每1000人配备的医院病床数。资料来源：ESRI：美国医院病床仪表板
    - ICUs/1000人:	每1000人有ICU床位数。资料来源：ESRI：美国医院病床仪表板。MTI 找不到具有此指标每日或每周更新的源。
    - 通风机需求*:	COVID-19 患者所需的呼吸机数量。资料来源：IHME COVID-19预测。

    - 失业申请/1000人:	每周新失业保险申请/1000名工人。资料来源：劳工部。
    - 失业率:	                每周更新一次失业率。由 MTI 计算，并定期调整以匹配联邦机构统计数据。
    - 在家工作的百分比*:	根据 UMD 模型在家工作的劳动力百分比。根据工作旅行和失业申请的变化由 MTI 计算。
    - 累计通货膨胀率:	总体经济状况，由COVID-19疫情以来的累计通货膨胀率衡量。根据劳工统计局的CPI数据计算MTI。
    - 消费变化百分比*:	根据观察到的以代理方式前往各类消费站点的行程变化，从大流行前的基线中观察到的消费百分比变化。由 MTI 计算。

    - 60岁以上人口的百分比*:	60岁以上人口的百分比。资料来源：人口普查局。
    - 收入中位数:	收入中位数。资料来源：人口普查局。
    - 非裔美国人百分比:	非裔美国人的百分比。资料来源：人口普查局。
    - 西班牙裔美国人百分比:	拉美裔美国人的百分比。资料来源：人口普查局。
    - 男性百分比:	男性百分比。资料来源：人口普查局。
    - 人口密度:		人口密度。资料来源：人口普查局。
    - 就业密度:		就业密度。来源：智能位置数据库。
    - 热点/1000: 人	每 1000 人聚集人群的兴趣点数。由 MTI 计算。
    - COVID 死亡率*:	在所有COVID-19病例中死亡的百分比。由 MTI 根据死亡人数和估计的 COVID 病例总数（包括确诊和未经测试的病例）计算。
    - 人口:	                州或县的总人口。资料来源：人口普查局。
