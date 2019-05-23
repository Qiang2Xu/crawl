import requests, sys, os, json, re
from jsonpath import jsonpath
from bs4 import BeautifulSoup
from multiprocessing.pool import Pool


headers = {
	'Host': 'interface.sina.cn',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
	'Referer': 'https://gif.sina.com.cn/',
	'Connection': 'keep-alive',
	'Cookie': 'ustat=__10.13.32.188_1557408552_0.00047000; genTime=1557408552; vt=4',
	'Accept-Encoding': 'gzip, deflate'
	}

certFile = r'C:\Users\XuQ\Desktop\2.crt'

# 非法字符去除
def validateTitle(title):
	rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
	new_title = re.sub(rstr, "_", title)  # 替换为下划线
	return new_title

def fetch_img(page):
	
	url = 'https://interface.sina.cn/tech/gif/album.d.json?format=json&num=6&page={0}&jsoncallback=getDataJson'.format(page)
		
	r = requests.get(url, headers=headers, verify=certFile)
	json_str = r.text[12:-1]
	data_unicode = json.loads(json_str)
	titles = jsonpath(data_unicode, "$..name")
	imgs = jsonpath(data_unicode, "$..img_url")
	
	for img, title in zip(imgs,titles):
		if img[:6] != "https:":
			img = "https:" + img
		
		data = {
			'title': title,
			'img': img,
			}
		print(data)
		resp = requests.get(img, verify=certFile)
		path = os.path.join('E:/img',str(page))
		if not os.path.exists(path):
			os.makedirs(path)
		os.chdir(path)
		
		with open(validateTitle(title)+'.gif', 'wb') as f:
			f.write(resp.content)
		
		
if __name__ == "__main__":
	pool = Pool()
	pages = list(range(1,6))
	pool.map(fetch_img, pages)
	pool.close()
	pool.join()

