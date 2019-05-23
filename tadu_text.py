import requests, sys
from bs4 import BeautifulSoup
from urllib.request import urljoin
import bs4

class tadu(object):
	
	def __init__(self, url):
		self.server = 'http://www.tadu.com/'
		self.url = url
		self.names = []
		self.urls = []
		self.nums = 0
		self.headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/71.0.3578.98 Safari/537.36' ,'Connection': 'close'}
		self.certFile = r'C:\Users\XuQ\Desktop\2.crt'
		
	def get_page_url(self):
		r = requests.get(self.url, headers=self.headers, verify=self.certFile)
		html = r.text
		soup = BeautifulSoup(html,'lxml')
		for a in soup.find('div',{'class':'chapter clearfix'}).find_all('a'):
			self.names.append(a.string)
			self.urls.append(urljoin(self.server, a['href']))
			self.nums += 1
		
	def get_text_url(self, url):
		# 提取存放小说文本的URL，ajax
		r = requests.get(url, headers=self.headers, verify=self.certFile)
		html = r.text
		soup = BeautifulSoup(html,'lxml')
		text_url = soup.find(id="bookPartResourceUrl")
		if not text_url:
			return self.get_text_url(url)
		return text_url['value']
	
	def get_text(self, text_url):
		
		r1 = requests.get(text_url, headers=self.headers, verify=self.certFile)
		r1.encoding = r1.apparent_encoding
		html = r1.text.replace('<p>','\n').replace('</p>','\n')
		return html[20:-3]
		
	def writer(self, name, path, text):
		with open(path, 'a') as f:
			f.write(name + '\n')
			f.write(text)
			f.write('\n\n')

if __name__=="__main__":
	url = 'http://www.tadu.com/book/catalogue/549768'
	path = "E:/三国大主播（免费）.txt"
	t = tadu(url)
	t.get_page_url()
	for i in range(t.nums):
		text_url = t.get_text_url(t.urls[i])
		t.writer(t.names[i], path, t.get_text(text_url))
		sys.stdout.write("  已下载:%.3f%%" %  float(i/t.nums) + '\r')
		sys.stdout.flush()
