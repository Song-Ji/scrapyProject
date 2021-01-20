# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib.request
import os
import re
import pyodbc
import time



#file_path是access文件的绝对路径
file_path = r'D:\Download\Database1.accdb'
#host是新闻速递首页的url
host = 'http://news.skykiwi.com/na/index.shtml'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
#local_path是抓取图片存储的根目录
local_path = r"C:\Users\focus\Downloads\imgs"




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



def get_info_stuff(url):
	"""get title, publish date, content, image of the article """
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
	response = requests.get(url, headers)  # 发起网络请求，获得响应
	response.encoding = 'utf-8'  # 网页编码
	soup = BeautifulSoup(response.text, 'html.parser')  # 使用BeautifulSoup解析，查找想要的内容。html.parser是熊内置的解析方案，可以不填会有warning
	title = soup.find('h1').text.strip().replace("'","''")
	print(title)
	timestamp = soup.find('span', {'itemprop': 'dateModified'}).text
	print(timestamp)
	source = 'Stuff'
	original_author = soup.find('span', {'itemprop': 'name'}).text
	print(original_author)
	"""正文包含视频链接"""
	content = soup.find('p', {'class': 'sics-component__html-injector sics-component__story__intro sics-component__story__paragraph'}).text.strip()
	for p_node in soup.find('span', {'class': 'sics-component__story__body sics-component__story__body--nativform'}).findAll('p', {'class': 'sics-component__html-injector sics-component__story__paragraph'}):
		content += '\n' + '\n' + p_node.text.strip()
	content = content.replace("'","''")
	print(content)
	get_img(soup.find('span', {'class': 'sics-component__story__body sics-component__story__body--nativform'}).findAll('meta', {'itemprop': 'url'}), url)
	return {'url': url, 'title': title, 'date_publish': timestamp, 'from': source, 'original_author': original_author, 'content': content}



def get_info_herald(url):
	"""get title, publish date, content, image of the article """
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
	response = requests.get(url, headers)  # 发起网络请求，获得响应
	response.encoding = 'utf-8'  # 网页编码
	soup = BeautifulSoup(response.text, 'html.parser')  # 使用BeautifulSoup解析，查找想要的内容。html.parser是熊内置的解析方案，可以不填会有warning
	title = soup.find('h1', {'class': 'article__heading'}).text.strip().replace("'","''")
	print(title)
	timestamp = soup.find('time', {'class': 'meta-data__time-stamp'}).text
	print(timestamp)
	source = 'NZherald'
	original_author = soup.find('div', {'class': 'author__name'}).text
	print(original_author)
	"""正文包含视频链接"""
	content = ''
	for p_node in soup.find('section', {'class': 'article__body full-content article__content'}).findAll('p'):
		content += p_node.text.strip() + '\n' + '\n'
	content = content.strip().replace("'","''")
	print(content)
	imgs = []
	for figure_node in soup.find('section', {'class': 'article__body full-content article__content'}).findAll('figure', {'class': 'figure'}):
		imgs.append(figure_node.find('img'))
	get_img(imgs, url)
	return {'url': url, 'title': title, 'date_publish': timestamp, 'from': source, 'original_author': original_author, 'content': content}

'https://resources.stuff.co.nz/content/dam/images/4/y/q/j/p/5/image.related.StuffLandscapeSixteenByNine.710x400.21tu26.png/1611116981308.jpg?format=pjpg&optimize=medium'

'https://www.nzherald.co.nz/nz/auckland-transport-unveils-fleet-of-electric-buses-for-new-airportlink-service/QB4EUKXIH5P3V6R533GGEUETDU/'

'https://www.nzherald.co.nz/resizer/N6_1u7pnAjT62oFPukgsy2-oZmI=/16x11/smart/filters:quality(70)/cloudfront-ap-southeast-2.images.arcpublishing.com/nzme/ZL4X4Q4LYBPK5EDNFCGU3UBMIQ.jpg'

def mkdir(path):
	"""create directories to save images"""
	folder = os.path.exists(path)

	if not folder:
		os.makedirs(path)
		return True
	else:
		print('--- folder already exists ---')
		return False
' 16w,'


def get_img(imgs, url):
	"""创建文章的文件夹保存图片"""
	if imgs:
		img_src = ''
		folder_path = local_path + '\\' + url.split('/')[-2]
		if mkdir(folder_path):
			for index, img in enumerate(imgs):
				if img.get('content'):
					img_src = img.get('content').split('?')[0]
				else:
					img_src = img.get('data-srcset').strip().split(' ')[2]
					img_src = img_src.strip().replace('320w,', '')
				print(img_src)
				try:
					if img_src[-3:] == 'gif':
						img_name = folder_path+'\\'+str(index + 1)+'.gif'
						urllib.request.urlretrieve(img_src, img_name)
					elif img_src[-3:] == 'png':
						img_name = folder_path+'\\'+str(index + 1)+'.png'
						urllib.request.urlretrieve(img_src, img_name)
					elif img_src[-4:] == 'jpeg':
						img_name = folder_path+'\\'+str(index + 1)+'.jpeg'
						urllib.request.urlretrieve(img_src, img_name)
					else:
						img_name = folder_path+'\\'+str(index + 1)+'.jpg'
						urllib.request.urlretrieve(img_src, img_name)
				except Exception as ex:
					print("出现如下异常: %s" % ex)
					print("文件下载保存到本地出错")
					print("Img Src: "+ img_src)
					print("Directory: " + img_name)
					print("URL: "+ url)


# def get_img_herald(imgs, url):
# 	"""创建文章的文件夹保存图片"""
# 	if imgs:
# 		folder_path = local_path + '\\' + url.split('/')[-2]
# 		if mkdir(folder_path):
# 			for index, img in enumerate(imgs):
# 				img_src = img.get('content').split('?')[0]
# 				print(img_src)
# 				try:
# 					if img_src[-3:] == 'gif':
# 						img_name = folder_path+'\\'+str(index + 1)+'.gif'
# 						urllib.request.urlretrieve(img_src, img_name)
# 					elif img_src[-3:] == 'png':
# 						img_name = folder_path+'\\'+str(index + 1)+'.png'
# 						urllib.request.urlretrieve(img_src, img_name)
# 					elif img_src[-4:] == 'jpeg':
# 						img_name = folder_path+'\\'+str(index + 1)+'.jpeg'
# 						urllib.request.urlretrieve(img_src, img_name)
# 					else:
# 						img_name = folder_path+'\\'+str(index + 1)+'.jpg'
# 						urllib.request.urlretrieve(img_src, img_name)
# 				except Exception as ex:
# 					print("出现如下异常: %s" % ex)
# 					print("文件下载保存到本地出错")
# 					print("Img Src: "+ img_src)
# 					print("Directory: " + img_name)
# 					print("URL: "+ url)



def save_info_to_db(info_list):
	'''将获取到的文章信息存储到数据库'''
	conn = pyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+file_path)
	cursor=conn.cursor()
	#创建表格
	# try:
	# 	cursor.execute("CREATE TABLE skykiwi_table(url Text, title Text, date_publish Text, body Memo, contents Memo)")
	# 	conn.commit()
	# except:
	# 	print("出现如下异常: %s" % ex)
	# 	print("创建表格失败")
	# 	return False
	for info in info_list:
		url = info.get('url')
		title = info.get('title')
		date_publish = info.get('date_publish')
		body = info.get('body')
		contents = info.get('contents')
		#sql query if the title is already in the table
		result = cursor.execute("SELECT * FROM skykiwi_table WHERE url = '%s'" % url)
		data = result.fetchall()
		try:
			if not data:
				sql = "INSERT INTO skykiwi_table VALUES('%s', '%s', '%s', '%s', '%s')" % (url, title, date_publish, body, contents)
				cursor.execute(sql)
				conn.commit()
		except Exception as ex:
			print("出现如下异常: %s" % ex)
			print("数据保存失败")
			print("Title: "+ title)
			print("URL: "+ url)
	# try:
	# 	# 执行sql语句
	# 	提交到数据库执行
	# except:
	# 	# 如果发生错误则回滚
	# conn.rollback()
	# cur = cursor.execute('select * from myTable')
	# # 获取数据库中表的全部数据
	# data= cur.fetchall()
	# print(data)
	#关闭游标和链接
	cursor.close()
	conn.close()



def main():
	'''main function'''
	info_list = []
	for url in get_urls(host):
		info_list.append(get_info(url))
		time.sleep(10)
	# save_info_to_db(info_list)
	# info_list.clear()



# if __name__ == '__main__':
# 	main()




get_info_herald('https://www.nzherald.co.nz/hawkes-bay-today/news/bay-view-bp-fire-woman-says-stranger-seeking-ride-placed-bucket-of-fuel-on-passengers-lap/KI7ASO7DXYLI73WIOADTHPC7Z4/')