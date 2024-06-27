import csv
import json
import time

import requests
from fake_useragent import UserAgent

# 成绩筛选阈值
score_threshold = 25
score_low_threshold = 50
section_threshold = 40000
section_low_threshold = 40000
# 晨晨成绩
chengchen_score = 503
chenchen_section = 120000

# 提取每一科的分数
year = 2023  # 23年成绩
area = 13  # 13代表河北

csv_res = []


# 根据页面获取请求头和url
def get_config(page):
    # 打开你的json文件
    headers = {"Accept": "application/json, text/plain, */*",
               "User-Agent": UserAgent().random}
    # TODO
    url = "https://api.zjzw.cn/web/api/?keyword=&page={}&province_id=&ranktype=&request_type=1&size=20&top_school_id=[120,3703,227,1400,3117,1398,1724,597,602,721]&type=&uri=apidata/api/gkv3/school/lists&signsafe=4f2c6c77a052acdee5fa718fe75f05ef".format(
        page)
    return headers, url


# 获取响应体
def request_api(url, header):
    try:
        response = requests.post(url, headers=header)
        if response.status_code == 200:
            return response.text
        else:
            print(f"请求失败，状态码：{response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"请求出现异常：{e}")
        return None


# 提取学校相关信息
def extract_info(text: str):
    # 解析json
    data = json.loads(text)
    if not data['data']:
        print("查询不到学校信息")
        return
    for schoolInfo in data['data']['item']:  # ['numFound']总条数
        # print(schoolInfo)

        # 提取学校id，get请求使用
        school_id = schoolInfo['school_id']
        # 提取学校名称
        high_title = schoolInfo['hightitle']
        # 提取学校是否公办或者民办
        nature_name = schoolInfo['nature_name']
        # 提取学校地址
        address = schoolInfo['province_name'] + "省" + schoolInfo['city_name'] + schoolInfo['county_name']
        # 提取学校是否是985，211，双一流
        ifDual = (schoolInfo['dual_class_name'] != "")
        if985 = (schoolInfo['f985'] == 1)
        if211 = (schoolInfo['f211'] == 1)

        headers = {"Accept": "application/json, text/plain, */*",
                   "User-Agent": UserAgent().random}
        # TODO
        url = "https://static-data.gaokao.cn/www/2.0/schoolspecialscore/{}/{}/{}.json".format(school_id, year, area)
        r = requests.get(url=url)
        r2 = r.text.encode().decode('unicode_escape')
        try:
            data = json.loads(r2)
        except Exception as e:
            print("未查询到" + high_title + "相关信息")
            continue
        print(data)

        def get_code(code1, code2):
            code1_list = {"物理类": 73, "历史类": 74}
            code2_list = {"本科批": 14, "本科提前批": 37, '专科批': 10}
            return "20" + str(code1_list[code1]) + "_" + str(code2_list[code2]) + "_0"

        # 看晨晨想不想上专科
        code_list = [get_code("物理类", "本科批"), get_code("物理类", "专科批")]
        # 获取每个专业的专业名称，录取批次，最低分，最低位次，录取要求  [2073_14_0]  73: 物理类 74：历史类  14：本科批 37：提前批
        for code_list_item in code_list:
            if data['data'].get(code_list_item):
                for item in data['data'][code_list_item]['item']:
                    name = item['level1_name'] + ", " + item['level2_name'] + ", " + item['level3_name']
                    min = item['min']  # 最低分
                    min_section = int(item['min_section'])  # 最低录取批次
                    request = item['sp_info']  # 录取要求

                    # TODO 判断逻辑
                    # 分数相差不超过score_threshold
                    # 名次相差不超过section_threshold
                    if ((min - chengchen_score < score_threshold) and (
                            chengchen_score - min < score_low_threshold)) or ((
                                                                                      chenchen_section - min_section < section_threshold) and (
                                                                                      min_section - chenchen_section < section_low_threshold)) and xnor(
                        request.find("首选") != -1,
                        request.find("物理")) != -1:
                        res = {}
                        res['school_name'] = high_title
                        res['nature_name'] = nature_name
                        res['address'] = address
                        res['ifDual'] = ifDual
                        res['if985'] = if985
                        res['if211'] = if211
                        res['name'] = name
                        res['min'] = min
                        res['min_section'] = min_section
                        res['request'] = request
                        csv_res.append(res)

        time.sleep(0.5)
def xnor(a, b):
    return (a and b) or (not a and not b)


def write_csv(lst):
    # 指定CSV文件的路径
    csv_file = 'data.csv'

    # CSV文件的表头，即字典的键
    if len(lst) == 0:
        print("表为空")
        return
    new_headers = {"school_name": "学校名称", "nature_name": "办学类型", "address": "学校地址", "ifDual": "双一流",
                   "if985": "985", "if211": "211", "name": "专业名称", "min": "2023年最低录取分数线",
                   "min_section": "2023年最低录取批次", "request": "录取要求"}
    fields = new_headers.values()
    # 写入CSV文件
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)

        # 写入表头
        writer.writeheader()

        # 逐行写入数据
        for row in lst:
            renamed_row={}
            for k,v in new_headers.items():
                renamed_row[v]=row[k]
            writer.writerow(renamed_row)


if __name__ == '__main__':
    for i in range(1,148):
        headers, url = get_config(i)
        text = request_api(url, headers)
        extract_info(text)
    write_csv(csv_res)
    pass
