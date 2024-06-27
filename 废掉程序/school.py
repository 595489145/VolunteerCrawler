# 导入所需模块
import json
import time
from time import sleep
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from requests_html import HTMLSession,UserAgent
import random
import os


def get_size(page=1):
    url = 'https://api.eol.cn/gkcx/api/?access_token=&admissions=&central=&department=&dual_class=&f211=&f985=&is_doublehigh=&is_dual_class=&keyword=&nature=&page={0}&province_id=&ranktype=&request_type=1&school_type=&signsafe=&size=20&sort=view_total&top_school_id=[2941]&type=&uri=apidata/api/gk/school/lists'\
        .format(page)
    session = HTMLSession()   #创建HTML会话对象
    user_agent = UserAgent().random  #创建随机请求头
    header = {"User-Agent": user_agent}
    res = session.post(url, headers=header)
    data = json.loads(res.text)
    size = 0
    if data["message"] == '成功---success':
        size = data["data"]["numFound"]
    return size

def get_university_info(size, page_size=20):
    page_cnt = int(size/page_size) if size%page_size==0 else int(size/page_size)+1
    print('一共{0}页数据，即将开始爬取...'.format(page_cnt))
    session2 = HTMLSession()   #创建HTML会话对象
    df_result = pd.DataFrame()
    for index in range(1, page_cnt+1):
        print('正在爬取第 {0}/{1} 页数据'.format(index, page_cnt))
        url = 'https://api.eol.cn/gkcx/api/?access_token=&admissions=&central=&department=&dual_class=&f211=&f985=&is_doublehigh=&is_dual_class=&keyword=&nature=&page={0}&province_id=&ranktype=&request_type=1&school_type=&signsafe=&size=20&sort=view_total&top_school_id=[2941]&type=&uri=apidata/api/gk/school/lists' \
            .format(index)
        user_agent = UserAgent().random  #创建随机请求头
        header = {"User-Agent": user_agent}
        res = session2.post(url, headers=header)

        with open("res.text", "a+", encoding="utf-8") as file:
            file.write(res.text)

        data = json.loads(res.text)

        if data["message"] == '成功---success':
            df_data = pd.DataFrame(data["data"]["item"])
            df_result = pd.concat([df_result, df_data], ignore_index=True)
            time.sleep(random.randint(5, 7))

    return df_result

size = get_size()
df_result = get_university_info(size)
df_result.to_csv('全国大学数据.csv', encoding='gbk', index=False)