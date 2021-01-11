# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib.request
import os
import re
import pyodbc




#file_path是access文件的绝对路径
file_path = r'D:\Download\Database1.accdb'
#host是新闻速递首页的url
host = 'https://www.6parknews.com/newspark/index.php'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
#local_path是抓取图片存储的根目录
local_path = 'D:\\Desktop\\img_news'




def mkdir(path):
	"""create directories to save images"""
	folder = os.path.exists(path)

	if not folder:
		os.makedirs(path)
		return True
	else:
		print('--- folder already exists ---')
		return False



def get_urls():
	url_list = []
	"""从新闻速递首页获取文章URL"""
	response = requests.get(host, headers)  # 发起网络请求，获得响应
	soup = BeautifulSoup(response.text, 'html.parser') # 使用BeautifulSoup解析，查找想要的内容。html.parser是熊内置的解析方案，可以不填会有warning
	div_node = soup.find('div', {'id': 'd_list'})  # 查找id值为d_list的div标签，
	ul_node = div_node.find('ul')  # 在div标签下查找第一个ul标签
	for li_node in ul_node.findAll('li'):  # 使用find_all()找出所有<li>标签，在for循环中解析每个<li>标签
		href = li_node.find('a')['href']  # 打印出li标签链接（href属性的值）
		if 'newspark' in href:
			url_article = urljoin(response.url, href) # response.url是响应的地址，不一定是原始请求地址哦，因为网站可能会把对请求做重定向
			url_list.append(url_article)
	return url_list



def get_info(url):
	"""get title, publish date, content, image of the article """
	response = requests.get(url, headers)  # 发起网络请求，获得响应
	response.encoding = 'utf-8'  # 网页编码
	soup = BeautifulSoup(response.text, 'html.parser')  # 使用BeautifulSoup解析，查找想要的内容。html.parser是熊内置的解析方案，可以不填会有warning
	title = soup.find('h2', {'style': 'margin:15px;text-align:center;'}).text
	# timestamp = soup.find('p', {'style': 'padding:5px;'}).text
	# result = re.findall(".*于(.*)大.*", soup.find('p', {'style': 'padding:5px;'}).text)
	timestamp = "".join(re.findall(".*于(.*)大.*", soup.find('p', {'style': 'padding:5px;'}).text)).rstrip()
	"""内容包含正文以及视频链接"""
	content = get_vid_link(soup.find('div', {'id': 'shownewsc'}).findAll('iframe')) + soup.find('div', {'id': 'shownewsc'}).text
	get_img(soup.find('div', {'id': 'shownewsc'}).findAll('img'), title)
	return {'url': url, 'title': title, 'date_publish': timestamp, 'content': content}



def get_img(imgs, title_article):
	"""创建文章的文件夹保存图片"""
	new_title_article = validateTitle(title_article)
	folder_path = local_path + '\\' + new_title_article
	if mkdir(folder_path):
		for index, img in enumerate(imgs):
			img_src = img.get('src')
			if img_src[-3:] == 'gif':
				img_name = folder_path+'\\'+str(index + 1)+'.gif'
				urllib.request.urlretrieve(img_src, img_name)
			elif img_src[-3:] == 'png':
				img_name = folder_path+'\\'+str(index + 1)+'.png'
				urllib.request.urlretrieve(img_src, img_name)
			else:
				img_name = folder_path+'\\'+str(index + 1)+'.jpg'
				urllib.request.urlretrieve(img_src, img_name)



def get_vid_link(vid_links):
	video_links = ''
	if vid_links:
		for video in vid_links:
			video_src = video.get('src')
			video_links += video_src + '[v]'
	else:
		print('there is no video links in the article')
	return video_links



def validateTitle(title):
	"""替换字符串中不能用于文件名的字符"""
	rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
	new_title = re.sub(rstr, "_", title)  # 替换为下划线
	return new_title



def save_info_to_db(info_list):
	'''将获取到的文章信息存储到数据库'''
	conn = pyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+file_path)
	cursor=conn.cursor()
	#创建表格
	cursor.execute("CREATE TABLE myTable(url Text, title Text, date_publish Text, content Memo)")
	for info in info_list:
		#sql query if the title is already in the table
		result = cursor.execute("SELECT * FROM myTable WHERE url = '%s'" % (info.get('url')))
		data = result.fetchall()
		if not data:
			sql = "INSERT INTO myTable VALUES('%s', '%s', '%s', '%s')" % (info.get('url'), info.get('title'), info.get('date_publish'), info.get('content'))
			cursor.execute(sql)
	# try:
	# 	# 执行sql语句
	# 	提交到数据库执行
	conn.commit()
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
	for url in get_urls():
		info_list.append(get_info(url))
	save_info_to_db(info_list)



if __name__ == '__main__':
	main()

# string = "新闻来源: 中国日报 于2021-01-11 0:14:26        大字阅读 提示:新闻观点不代表本网立场"
# result = re.findall(".*于(.*)大.*",string)

# result= "".join(re.findall(".*于(.*)大.*",string)).rstrip()

# print(len(result))

# print(result)






# def test():
# 	conn = pyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+file_path)
# 	cursor=conn.cursor()
# 	#创建表格
# 	# cursor.execute("CREATE TABLE myTable(url Text, title Text, date_publish Text, content Memo)")
# 	# result = cursor.execute("SELECT * FROM myTable WHERE url = '%s'" % ("sss"))
# 	# data = result.fetchall()
# 	cursor.execute("drop table myTable")
# 	# for info in info_list:
# 	# 	#sql query if the title is already in the table
# 	# 	if "SELECT * FROM myTable WHERE url = '%s'" % (info.get('url')) is None:
# 	# 		sql = "INSERT INTO myTable VALUES('%s', '%s', '%s', '%s')" % (info.get('url'), info.get('title'), info.get('date_publish'), info.get('content'))
# 	# 		cursor.execute(sql)
# 	conn.commit()
# 	cursor.close()
# 	conn.close()
# test()



# dic = get_info('https://www.6parknews.com/newspark/view.php?app=news&act=view&nid=460373')


# str = test('https://www.6parknews.com/newspark/view.php?app=news&act=view&nid=460358')
# print(str)


# t = 'jisong'
# path = 'D:\\Desktop\\img_news\\'+t
# # os.makedirs(path)
# img_src = 'https://web.popo8.com/202101/06/10/fad69fb394.jpg'
# urllib.request.urlretrieve(img_src, path+'\\%s.jpg')



#"D:\Desktop\img_news"
