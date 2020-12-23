# -*- coding: utf-8 -*-
from urllib import request  # 导入urllib中的request模块
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# response = request.urlopen('http://youxiputao.com/')  # 用urlopen()函数执行一次请求，地址是游戏葡萄的首页，并把返回对象赋值给response变量。
# html = response.read().decode()  # 从response中读取结果，解码成str类型的字符串，就是我们的html源码。
# print(html)  # 在控制台打印html源码。

response = requests.get('https://www.6park.com/nz.shtml')  # 发起网络请求，获得响应
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')  # 使用BeautifulSoup解析，查找想要的内容。html.parser是熊内置的解析方案，可以不填会有warning
td_node = soup.find('td', {'class': 'td5'})  # 查找class值为td5的td标签，
div_node = td_node.find('div')  # 在td标签下查找第一个div标签
for a_node in div_node.findAll('a'):  # 使用find_all()找出所有<a>标签，在for循环中解析每个<a>标签
    title = a_node.text  # 打印出a标签内容
    href = a_node['href']  # 打印出a标签链接（href属性的值）
    url = urljoin(response.url, href)  # response.url是响应的地址，不一定是原始请求地址哦，因为网站可能会把对请求做重定向
    print(url, title)


