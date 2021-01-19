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

