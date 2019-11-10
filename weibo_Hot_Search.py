# -*- coding=utf8 -*-
#!usr/bin/env python
# 每天爬取两次，时间点分别为上午十一点和晚上十一点
# 不要问我为什么选择这两个时间点，因为总感觉这两个时间点会爆出来大事情

import os
import time
import requests
from lxml import etree

url = "https://s.weibo.com/top/summary?cate=realtimehot"
headers={
    'Host': 's.weibo.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'https://weibo.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}

r = requests.get(url,headers=headers)
print(r.status_code)

html_xpath = etree.HTML(r.text)
data = html_xpath.xpath('//*[@id="pl_top_realtimehot"]/table/tbody/tr/td[2]')
num = -1


# 解决存储路径
time_path = time.strftime('%Y{y}%m{m}%d{d}',time.localtime()).format(y='年', m='月', d='日')
time_name = time.strftime('%Y{y}%m{m}%d{d}%H{h}',time.localtime()).format(y='年', m='月', d='日',h='点')
root = "./" + time_path + "/"
path = root + time_name + '.md'
if not os.path.exists(root):
    os.mkdir(root)


# 文件头部信息
with open(path,'a') as f:
    f.write('{} {}\n\n'.format('# ',time_name+'数据'))
f.close()

for tr in (data):
    title = tr.xpath('./a/text()')
    hot_score = tr.xpath('./span/text()')
    
    num += 1

    # 过滤第 0 条
    if num == 0:
        pass
    else:
        with open(path,'a') as f:

            f.write('{} {}、{}\n\n'.format('###',num,title[0]))
            f.write('{} {}\n\n'.format('微博当时热度为：',hot_score[0]))
         
        f.close()

        print(num,title[0],'微博此时的热度为：',hot_score[0])
