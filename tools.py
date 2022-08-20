# -*- coding: utf-8 -*-
# @Time    : 2022/8/19 0019 13:21
# @Author  : Leo.W
# @Email   : wanglei@whu.edu.cn
# @File    : tools.py

import os
import pandas as pd
from datetime import datetime


def fun_files(path):
    """
    遍历日志文件夹文件，程序若发生中断可以接着上次的时间段继续爬取
    """
    fileArray = []
    for root, dirs, files in os.walk(path):
        for fn in files:
            eachpath = str(fn)
            fileArray.append(eachpath)
    # print(fileArray)
    return fileArray


def read_txt(path):
    """
    按行读取文本，返回列表
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
        data = [i.strip('\n').strip() for i in data]
    return data


def searchInfoCSV(f_keyword, db_name, title, caption_cite, caption_time, caption_p, csv_path):
    id = [i for i in range(len(title))]
    if not os.path.exists(csv_path):
        os.mkdir(csv_path)
    save_csv_path = csv_path + '/' + f'{f_keyword}_{db_name}.csv'
    DATA = {
        'title': title,
        'caption_cite': caption_cite,
        'caption_time': caption_time,
        'caption_p': caption_p,
    }
    col_names = ['title', 'caption_cite', 'caption_time', 'caption_p']
    save = pd.DataFrame(DATA, index=id, columns=col_names)
    save.to_csv(save_csv_path, sep=',')


def getStart(api):
    """
    获取起始日期，用于分段抓取
    程序中断后可通过判断日志文件的日期位置，自动继续爬取后面日期内容
    """
    data = pd.read_csv('filter.csv')
    start_list = list(data['start'])
    end_list = list(data['end'])
    output_log_path = api.conf['output_log_path']
    if not os.path.exists(output_log_path):
        os.mkdir(output_log_path)
    log_list = fun_files(output_log_path)
    if log_list:
        # 判断最后一条log文件
        end_log_txt_path = output_log_path + '/' + log_list[0]
        end_log_txt_data = read_txt(end_log_txt_path)
        broken_pos_start = list(log_list[0].split('.')[0].split('_')[2])
        broken_pos_end = list(log_list[0].split('.')[0].split('_')[3])
        # log文件名中的日期信息与filter.csv格式一致化
        if broken_pos_start[4] == '0':
            broken_pos_start[4] = '/'
            if broken_pos_start[6] == '0':
                broken_pos_start[6] = '/'
            else:
                broken_pos_start.insert(6, '/')
        else:
            broken_pos_start.insert(4, '/')
            if broken_pos_start[7] == '0':
                broken_pos_start[7] = '/'
            else:
                broken_pos_start.insert(7, '/')
        if broken_pos_end[4] == '0':
            broken_pos_end[4] = '/'
            if broken_pos_end[6] == '0':
                broken_pos_end[6] = '/'
            else:
                broken_pos_end.insert(6, '/')
        else:
            broken_pos_end.insert(4, '/')
            if broken_pos_end[7] == '0':
                broken_pos_end[7] = '/'
            else:
                broken_pos_end.insert(7, '/')
        broken_pos_start = ''.join(broken_pos_start)
        broken_pos_end = ''.join(broken_pos_end)
        # 根据最后一条log文件是否抓取完毕，判断程序中断重开后的起始日期
        if end_log_txt_data == [] or end_log_txt_data[-1] != '------End------':
            start_list = start_list[start_list.index(broken_pos_start):]
            end_list = end_list[end_list.index(broken_pos_end):]
        else:
            start_list = start_list[start_list.index(broken_pos_start) + 1:]
            end_list = end_list[end_list.index(broken_pos_end) + 1:]
    return start_list, end_list




def getTime(_t):
    """
    caption_time中会出现如"7 hours ago"或"7 days ago"
    getTime(_t)将其处理成具体的时间
    如今天是2022/8/19，"7 hours ago"是2022/8/19，则返回值为“Aug 19, 2022”
    如今天是2022/8/19，"7 days ago"是2022/8/12，则返回值为“Aug 12, 2022”
    """
    list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    # # 当前时间的年月日
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    hour = datetime.now().hour
    if _t[0].find('hour') != -1:
        if _t[0].find('hours') != -1:
            # 前一天--闰年？--几月？--1号的前一天=28？29？31？30？
            h = int(_t[0].replace(' hours ago', '').strip())
        else:
            h = int(_t[0].replace(' hour ago', '').strip())
        if h >= hour:
            if month == 1:
                if day == 1:
                    month = 12
                    day = 31
                else:
                    day -= 1
            elif month == 3:
                if (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0):
                    if day == 1:
                        month = 2
                        day = 29
                    else:
                        day -= 1
                else:
                    if day == 1:
                        month = 2
                        day = 28
                    else:
                        day -= 1
            elif month == 2 or month == 4 or month == 6 or month == 8 or month == 9 or month == 11:
                if day == 1:
                    month -= 1
                    day = 31
                else:
                    day -= 1
            elif month == 5 or month == 7 or month == 10 or month == 12:
                if day == 1:
                    month -= 1
                    day = 30
                else:
                    day -= 1
            else:
                print(_t[0])
        month = list[month-1]
        time = ('{0} {1}, {2}'.format(month, day, year))

    elif _t[0].find('day') != -1:
        if _t[0].find('days') != -1:
            d = int(_t[0].replace(' days ago', '').strip())
        else:
            d = int(_t[0].replace(' day ago', '').strip())
        if month == 1:
            if day <= d:
                month = 12
                day = 31 - d + day
            else:
                day -= d
        elif month == 3:
            if (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0):
                if day <= d:
                    month = 2
                    day = 29 - d + day
                else:
                    day -= d
            else:
                if day <= d:
                    month = 2
                    day = 28 - d + day
                else:
                    day -= d
        elif month == 2 or month == 4 or month == 6 or month == 8 or month == 9 or month == 11:
            if day <= d:
                month -= 1
                day = 31 - d + day
            else:
                day -= d
        elif month == 5 or month == 7 or month == 10 or month == 12:
            if day <= d:
                month -= 1
                day = 30 - d + day
            else:
                day -= d
        else:
            print(_t[0])
        month = list[month - 1]
        time = ('{0} {1}, {2}'.format(month, day, year))
    else:
        time = _t[0].strip()

    return time


def parseHTML(s, title, caption_cite, caption_time, caption_p, output_log):
    """
    利用XPath解析网页结构中的数据字段元素
    :param title: 标题信息
    :param caption_cite: 二级链接
    :param caption_time: 发布时间
    :param caption_p:  摘要信息
    """
    content = s.xpath('//*[@id="rso"]/div[@class="MjjYud"] | //*[@id="rso"]/div[@class="hlcw0c"]')
    # print(len(content))
    for each in content:
        t = [i.xpath('string(.)') for i in
             each.xpath('.//div[@class="yuRUbf"]/a/h3[@class="LC20lb MBeuO DKV0Md"]')]
        if t:
            title.extend(t)
        else:
            continue
            # title.append('None')

        c = each.xpath('.//div[@class="yuRUbf"]/a/@href')
        if c:
            caption_cite.extend(c)
        else:
            caption_cite.append('None')

        # flex的特殊情況
        for j in range(len(t)):
            _t = [i.xpath('string(.)') for i in each.xpath(
                './/div[@class="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc"]/span[@class="MUxGbd wuQ4Ob WZ8Tjf"]/span')]
            if _t:
                _t = getTime(_t)
                caption_time.append(_t.strip())
            else:
                _t = [i.xpath('string(.)') for i in each.xpath(
                    './/div[@class="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf"]/span[@class="MUxGbd wuQ4Ob WZ8Tjf"]/span')]
                if _t:
                    _t = getTime(_t)
                    caption_time.append(_t.strip())
                else:
                    _t = [i.xpath('string(.)') for i in each.xpath(
                        './/div[@class="NJo7tc Z26q7c UK95Uc uUuwM"]/div[@class="MUxGbd wuQ4Ob WZ8Tjf"]/span')]
                    if _t:
                        _t = getTime(_t[0:1])
                        caption_time.append(_t.strip())
                    else:
                        caption_time.append('None')

            span_num = len(each.xpath('.//div[@class="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc"]/span'))
            if span_num == 2:
                p = [i.xpath('string(.)') for i in each.xpath(
                    './/div[@class="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc"]/span[last()]')]
                # print(p[0])
            elif span_num == 1:
                p = [i.xpath('string(.)') for i in each.xpath(
                './/div[@class="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc"]/span[@class="MUxGbd wuQ4Ob WZ8Tjf"]/span')]
                if p == []:
                    p = [i.xpath('string(.)') for i in each.xpath(
                        './/div[@class="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc"]/span')]
                elif p[0]:
                    p = each.xpath('.//div[@class="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc"]/text()')
                else:
                    p = [i.xpath('string(.)') for i in each.xpath(
                        './/div[@class="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc"]/span')]
            else:
                span_num = len(each.xpath('.//div[@class="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf"]/span'))
                if span_num == 2:
                    p = [i.xpath('string(.)') for i in each.xpath(
                        './/div[@class="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf"]/span[last()]')]
                    # print(p[0])
                elif span_num == 1:
                    p = [i.xpath('string(.)') for i in each.xpath(
                        './/div[@class="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf"]/span[@class="MUxGbd wuQ4Ob WZ8Tjf"]/span')]
                    if p == []:
                        p = [i.xpath('string(.)') for i in each.xpath(
                            './/div[@class="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf"]/span')]
                    elif p[0]:
                        p = each.xpath('.//div[@class="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf"]/text()')
                    else:
                        p = [i.xpath('string(.)') for i in each.xpath(
                            './/div[@class="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf"]/span')]
                else:
                    caption_p.append('None')
                    continue
            caption_p.append(p[0].replace('\ufeff', ''))
    # 数据字段信息应长度一致，否则为解析错误（可能是谷歌网页需要人机验证，可以点击失败的网页链接查看）
    # 有效解决方案：更换代理（可以是更换ip+端口，或者更换代理的节点）
    if(len(title) != len(caption_p)):
        print('Parse HTML falied, View line 294 in tools.py', file=output_log)
        print('Parse HTML falied, View line 294 in tools.py')

    print("title：{}\t\tcaption_cite：{}\t\tcaption_time：{}\t\tcaption_p：{}".format(len(title), len(caption_cite), len(caption_time), len(caption_p)), file=output_log)
    print("title：{}\t\tcaption_cite：{}\t\tcaption_time：{}\t\tcaption_p：{}".format(len(title), len(caption_cite), len(caption_time), len(caption_p)))
    print("-----------------------------------------------------------------------------------------------", file=output_log)
    print("-----------------------------------------------------------------------------------------------")
