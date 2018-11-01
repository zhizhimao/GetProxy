#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
创建时间：Sat Aug 18 15:31:10 2018
作者: 星空飘飘
平台：Anaconda 3-5.1.0
语言版本：Python 3.6.4
编辑器：Spyder
分析器：Pandas: 0.22.0
解析器：lxml: 4.1.1
数据库：MongoDB 2.6.12
程序名：getproxy.py

获取代理ip并检测可用代理保存文件proxy.txt
"""

import requests
import re
import threading


def get_xicidaili():
    # 获取西刺代理ip
    page = 'http://www.xicidaili.com/wt/'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400'}
    proxy_list = []
    for pg in range(1, 11):  # 获取前10页
        url = f'{page}{pg}'
        request = requests.get(url, headers=header)
        html = request.text
        proxy_ip = re.findall('<tr class=".*?<td>(\d+.\d+.\d+.\d+)</td>.*?<td>(\d+)</td>', html, re.S)
        for ip, prot in proxy_ip:
            ip_prot = '{0}:{1}'.format(ip, prot)
            proxy_list.append(ip_prot)
    return proxy_list


def check_proxy(proxy):
    # 验证代理ip
    url = 'http://2018.ip138.com/ic.asp'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400'}
    try:
        response = requests.get(url, proxies={'http': proxy}, headers=header, timeout=2)
        if response:
            response.encoding = response.apparent_encoding
            html = response.text
            ip = re.findall('<body style=.*?(\d+.\d+.\d+.\d+).*?</center></body></html>', html, re.S)
            print(proxy, ip)
            with open('proxy.txt', 'a') as f:
                f.write('{0}\n'.format(proxy))
            return proxy
    except Exception as error:
        return None


if __name__ == '__main__':
    proxy_list = get_xicidaili()  # 爬取代理
    threads = []  # 创建多线程列表
    for proxy in proxy_list:  # 添加线程任务
        threads.append(threading.Thread(target=check_proxy, args=(proxy, )))
    for t in threads:  # 运行线程任务
        t.setDaemon(False)  # 'False'主线程结束时检测该子线程是否结束,如果该子线程还在运行，则主线程会等待它完成后再退出.
        t.start()
