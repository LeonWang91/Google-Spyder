# -*- coding: utf-8 -*-
# @Time    : 2022/8/19 0019 16:29
# @Author  : Leo.W
# @Email   : wanglei@whu.edu.cn
# @File    : google_api.py


import random
import requests
import configparser
from tools import *


class Google():

    def __init__(self):
        self.conf = {}
        self.domain = './domain.txt' # 谷歌域名切换
        self.proxy = '127.0.0.1:7890' # 本机ip地址+代理端口（可以访问外网）
        self.proxies = {
            'http': 'http://{}'.format(self.proxy),
            'https': 'https://{}'.format(self.proxy)
        }
        self.headers = {
            'Content-type': "text/html;charset=utf-8",
            # 不建议随机更换user-agent，实际开发发现不同的user-agent解析的网页结构有些不同，部分标签无法解析到
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
            # 这里没有加cookies是因为在设置google翻页为50后，没有在response header中找到翻页页数的信息，实际爬取还是一页10条搜索结果
        }
        if os.path.exists('Config.ini'):
            print('[~] Read configuration file')
            config = configparser.ConfigParser()
            config.read("Config.ini", encoding='utf-8')
            self.conf['pn'] = config['config']['pn']
            self.conf['sl'] = config['config']['sl']
            self.conf['el'] = config['config']['el']
            self.conf['count'] = config['config']['count']
            self.conf['sleep'] = int(config['config']['sleep'])
            self.conf['output_log_path'] = config['config']['output_log_path']
            self.conf['output_log'] = config['config']['output_log']
            self.conf['csv_path'] = config['config']['csv_path']
            self.conf['keyword'] = config['config']['keyword']
            self.conf['save_flag'] = int(config['config']['save_flag'])
            print('[+] Read complete')
        else:
            print('[-] Configuration file not found')
            exit()


    def getHTML(self):
        """
            爬取网页源代码
        """
        url = ''
        retry_count = 5
        domain = read_txt(self.domain)
        f_keyword = self.conf['keyword'].replace(' ', '+')
        output_log = open(self.conf['output_log'], mode='a', encoding='utf-8')
        try:
            while retry_count > 0:
                try:
                    domains = random.choice(domain)
                    url = f"https://{domains}/search?hl=en&q={f_keyword}&tbs=cdr:1,cd_min%3A{self.conf['sl'][1]}/{self.conf['sl'][2]}/{self.conf['sl'][0]},cd_max:{self.conf['el'][1]}/{self.conf['el'][2]}/{self.conf['el'][0]}&start={str(self.conf['pn'])}"
                    r = requests.get(url, headers=self.headers, proxies=self.proxies, verify=False, timeout=30)
                    print(f"Page{int(self.conf['count'])}：{url}", file=output_log)
                    print(f"Page{int(self.conf['count'])}：{url}")
                    r.raise_for_status()
                    r.encoding = r.apparent_encoding
                    return r.content
                except Exception:
                    retry_count -= 1
        except:
            print(f"Get HTML Text Failed: {str(url)}", file=output_log)
            print(f"Get HTML Text Failed: {str(url)}")
