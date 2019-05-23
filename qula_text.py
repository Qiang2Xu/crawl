import requests, sys
from bs4 import BeautifulSoup
from urllib.request import urljoin
import bs4

class downloader(object):
	'''下载器的方法相同，仅仅修改了提取方法'''	
	def __init__(self, url):
		self.target = url
		self.names = []
		self.urls = []
		self.nums = 0
		
	def get_page_url(self):
		# 再次使用代理设置verify参数 不会出现代理错误的问题
		certFile  = r'C:\Users\XuQ\Desktop\2.crt'
		r = requests.get(url = self.target,verify =certFile)
		html = r.text
		soup = BeautifulSoup(html,'lxml')
		for a in soup.find('div', id='list').find_all('a'):
			self.names.append(a.string)
			self.urls.append(urljoin(self.target, a['href']))
			self.nums += 1

	def get_contents(self, name, target_url):
		print(target_url)
		headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/71.0.3578.98 Safari/537.36' ,'Connection': 'close'}
		certFile = r'C:\Users\XuQ\Desktop\2.crt'
		r = requests.get(url = target_url,  headers = headers,verify =certFile)
		html = r.text
		print('111111')
		soup = BeautifulSoup(html, 'lxml')
		text = soup.find('div', id='content')
		'''
		因为在响应中会随机出现None类型
		这里加了一个判断：如果不是Tag类型，
		就递归再次访问
		'''
		if isinstance(text, bs4.element.Tag):
			texts = str(text).replace('<br/>','\n').replace('<div id="content">','').replace('</div>','')
			return texts
		else:
			# print(name)
			return self.get_contents(name,target_url)
		
		
	def writer(self, name, path, text):
		with open(path, 'a', encoding = 'utf-8') as f:
			f.write(name + '\n')
			f.write(text)
			f.write('\n\n')
			
if __name__ == "__main__":
	url = 'https://www.qu.la/book/142465/'
	path = 'E:/止戈三国.txt'
	d1 = downloader(url)
	d1.get_page_url()
	print('《一年永恒》开始下载：')
	for i in range(d1.nums):
		d1.writer(d1.names[i], path, d1.get_contents(d1.names[i], d1.urls[i]))
		sys.stdout.write("  已下载:%.3f%%" %  float(i/d1.nums) + '\r')
		sys.stdout.flush()
	print('《止戈三国》下载完成')
