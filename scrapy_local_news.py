# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib.request
import os
import re
import pyodbc
import time




def get_urls():
	url_list_stuff = []
	url_list_herald = []
	host = 'https://news.google.com/topics/CAAqIggKIhxDQkFTRHdvSkwyMHZNR04wZDE5aUVnSmxiaWdBUAE?hl=en-NZ&gl=NZ&ceid=NZ%3Aen'
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
	"""从google news new zealand页面获取文章URL"""
	response = requests.get(host, headers)  # 发起网络请求，获得响应
	soup = BeautifulSoup(response.text, 'html.parser') # 使用BeautifulSoup解析，查找想要的内容。html.parser是熊内置的解析方案，可以不填会有warning
	#在google new上找到整个body的div，在这个div下面找每篇文章的div，在每篇文章的div下面找发布源和文章的链接。
	for div_node in soup.findAll('div'):
		if (div_node.get('jscontroller')) == 'd0DtYd' or (div_node.get('jslog') == 93789):
			publisher = div_node.find('div', {'class': 'SVJrMe'}).find('a').text
			if publisher == 'Stuff.co.nz':
				href_node = div_node.find('h3').find('a')
				url_article = 'https://news.google.com' + href_node['href'].replace('.', '')
				url_list_stuff.append(url_article)
			elif publisher == 'New Zealand Herald':
				href_node = div_node.find('h3').find('a')
				url_article = 'https://news.google.com' + href_node['href'].replace('.', '')
				 # response.url是响应的地址，不一定是原始请求地址，因为网站可能会把对请求做重定向
				# url_article = urljoin(response.url, href)
				url_list_herald.append(url_article)
			else:
				continue
	print('文章URL抓取完成')
	return {'stuff': url_list_stuff, 'herald': url_list_herald}



def get_urls_public_service():
	url_list = []
	host = 'http://bbs.skykiwi.com/forum.php?mod=forumdisplay&fid=205'
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
	"""从二手市场页面获取文章URL"""
	response = requests.get(host, headers)  # 发起网络请求，获得响应
	soup = BeautifulSoup(response.text, 'html.parser') # 使用BeautifulSoup解析，查找想要的内容。html.parser是熊内置的解析方案，可以不填会有warning
	table_node = soup.find('table', {'summary': 'forum_205'})  # 查找id值为d_list的div标签，
	for tbody_node in table_node.findAll('tbody'):  # 使用find_all()找出所有<li>标签，在for循环中解析每个<li>标签
		if tbody_node.has_attr('id'):
			if 'normalthread' in tbody_node['id']:
				href = tbody_node.find('th').findAll('a')[1]['href']
				url_article = urljoin(response.url, href) # response.url是响应的地址，不一定是原始请求地址哦，因为网站可能会把对请求做重定向
				url_list.append(url_article)
				# print(url_article)
	return url_list



def get_urls_job_recruitment():
	url_list = []
	host = 'http://bbs.skykiwi.com/forum.php?mod=forumdisplay&fid=55'
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
	"""从二手市场页面获取文章URL"""
	response = requests.get(host, headers)  # 发起网络请求，获得响应
	soup = BeautifulSoup(response.text, 'html.parser') # 使用BeautifulSoup解析，查找想要的内容。html.parser是熊内置的解析方案，可以不填会有warning
	table_node = soup.find('table', {'summary': 'forum_55'})  # 查找id值为d_list的div标签，
	for tbody_node in table_node.findAll('tbody'):  # 使用find_all()找出所有<li>标签，在for循环中解析每个<li>标签
		if tbody_node.has_attr('id'):
			if 'normalthread' in tbody_node['id']:
				href = tbody_node.find('th').findAll('a')[2]['href']
				url_article = urljoin(response.url, href) # response.url是响应的地址，不一定是原始请求地址哦，因为网站可能会把对请求做重定向
				url_list.append(url_article)
				print(url_article)
	return url_list



# def test():
# 	url_list_stuff = []
# 	url_list_herald = []
# 	host = 'https://news.google.com/topics/CAAqIggKIhxDQkFTRHdvSkwyMHZNR04wZDE5aUVnSmxiaWdBUAE?hl=en-NZ&gl=NZ&ceid=NZ%3Aen'
# 	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
# 	"""从google news new zealand页面获取文章URL"""
# 	response = requests.get(host, headers)  # 发起网络请求，获得响应
# 	soup = BeautifulSoup(response.text, 'html.parser') # 使用BeautifulSoup解析，查找想要的内容。html.parser是熊内置的解析方案，可以不填会有warning
# 	#在google new上找到整个body的div，在这个div下面找每篇文章的div，在每篇文章的div下面找发布源和文章的链接。
# 	for div_node in soup.findAll('div'):
# 		if (div_node.get('jscontroller')) == 'd0DtYd' or (div_node.get('jslog') == 93789):
# 			publisher = div_node.find('div', {'class': 'SVJrMe'}).find('a').text
# 			if publisher == 'Stuff.co.nz':
# 				href_node = div_node.find('h3').find('a')
# 				url_article = 'https://news.google.com' + href_node['href'].replace('.', '')
# 				print(url_article)
# 				url_list_stuff.append(url_article)
# 			elif publisher == 'New Zealand Herald':
# 				href_node = div_node.find('h3').find('a')
# 				url_article = 'https://news.google.com' + href_node['href'].replace('.', '')
# 				 # response.url是响应的地址，不一定是原始请求地址，因为网站可能会把对请求做重定向
# 				# url_article = urljoin(response.url, href)
# 				url_list_herald.append(url_article)
# 			else:
# 				continue
# 	print('文章URL抓取完成')
# 	return {'stuff': url_list_stuff, 'herald': url_list_herald}

# test()