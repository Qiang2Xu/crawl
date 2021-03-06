import requests, sys
from bs4 import BeautifulSoup
import bs4

class downloader(object):
	'''小说下载器'''
	def __init__(self, url):
		self.server = "https://www.biqukan.com/"
		self.target = url
		self.names = []
		self.urls = []
		self.nums = 0
		
	def get_page_url(self):
		# 使用代理时，设置verify参数 不会出现代理证书SSL错误的问题
		certFile  = r'C:\Users\XuQ\Desktop\2.crt'
		r = requests.get(url = self.target,verify =certFile )
		html = r.text
		soup = BeautifulSoup(html,'lxml')
		for a in soup.find('div', class_='listmain').find_all('a'):
			self.names.append(a.string)
			self.urls.append(self.server + a['href'])
			self.nums += 1

	def get_contents(self, name, target_url):
		# 
		certFile = r'C:\Users\XuQ\Desktop\2.crt'
		r = requests.get(url = target_url, verify =certFile, headers = {'Connection': 'close'})
		html = r.text
		soup = BeautifulSoup(html, 'lxml')
		text = soup.find('div', class_='showtxt')
		'''
		因为在响应中会随机出现None类型
		这里加了一个判断：如果不是Tag类型，
		就递归再次访问
		'''
		if isinstance(text, bs4.element.Tag):
			texts = text.get_text().replace('\xa0'*8,'\n\n\xa0\xa0')
			
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
	url = 'https://www.biqukan.com/1_1094/'
	path = 'E:/一念永恒.txt'
	d1 = downloader(url)
	d1.get_page_url()
	print('《一年永恒》开始下载：')
	for i in range(d1.nums):
		d1.writer(d1.names[i], path, d1.get_contents(d1.names[i], d1.urls[i]))

		sys.stdout.write("  已下载:%.3f%%" %  float(i/d1.nums) + '\r')
		sys.stdout.flush()
	print('《一年永恒》下载完成')
