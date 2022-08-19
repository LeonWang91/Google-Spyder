# -*- coding: utf-8 -*-
# @Time    : 2022/8/19 0019 13:22
# @Author  : Leo.W
# @Email   : wanglei@whu.edu.cn
# @File    : main.py


import time
import urllib3
from lxml import etree
import google_api
import searchInfo
from tools import *

urllib3.disable_warnings()


def HTML(api, start_list, end_list):
    f_keyword = api.conf['keyword'].replace(' ', '+')
    for i in range(len(start_list)):
        # 控制翻页
        api.conf['pn'] = 0
        page_inner = 'Next'
        # 数据字段
        title = []
        caption_cite = []
        caption_time = []
        caption_p = []
        # 区间
        sl = start_list[i].split('/')
        el = end_list[i].split('/')
        sl_month = '0' + sl[1] if 0 <= int(sl[1]) <= 9 else sl[1]
        el_month = '0' + el[1] if 0 <= int(el[1]) <= 9 else el[1]
        sl_day = '0' + sl[2] if 0 <= int(sl[2]) <= 9 else sl[2]
        el_day = '0' + el[2] if 0 <= int(el[2]) <= 9 else el[2]
        db_name = f'{sl[0]}{sl_month}{sl_day}_{el[0]}{el_month}{el_day}'
        api.conf['sl'] = sl
        api.conf['el'] = el
        # 写入日志
        api.conf['output_log'] = api.conf['output_log_path'] + '/' + f'log_{f_keyword}_{db_name}.txt'
        # 用于程序中断再运行清空上次文件内容
        output_log_1 = open(api.conf['output_log'], mode='w', encoding='utf-8')
        output_log = open(api.conf['output_log'], mode='a', encoding='utf-8')
        while page_inner:
            api.conf['count'] = api.conf['pn'] / 10 + 1
            time.sleep(api.conf['sleep'])
            html = api.getHTML()
            s = etree.HTML(html)
            parseHTML(s, title, caption_cite, caption_time, caption_p, output_log)
            # 控制翻页
            page_inner = s.xpath('//table[@class="AaVjTc"]//td[@class="d6cvqb BBwThe"]//span[text()="Next"]')
            if page_inner:
                api.conf['pn'] += 10
            else:
                break
        if api.conf['save_flag']:
            # 数据库文件保存
            searchInfo.db_import(f_keyword, db_name, title, caption_cite, caption_time, caption_p)
            print("------Stored in the database------", file=output_log)
            print("------Stored in the database------")
        else:
            # CSV文件保存
            csv_path = api.conf['csv_path']
            searchInfoCSV(f_keyword, db_name, title, caption_cite, caption_time, caption_p, csv_path)
            print("------Stored in the csv folder------", file=output_log)
            print("------Stored in the csv folder------")
        print("------End------", file=output_log)
        print("------End------")
        output_log.close()


if __name__ == '__main__':
    api = google_api.Google()
    start_list, end_list = getStart(api)
    HTML(api, start_list, end_list)



