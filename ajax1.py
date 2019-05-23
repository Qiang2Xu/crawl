import requests, sys, os
from bs4 import BeautifulSoup
from multiprocessing.pool import Pool


class downloader(object):
	
	def __init__(self):
		# self.server = 'http://www.tadu.com/'
		self.url = 'https://bcy.net/coser/index/ajaxloadtoppost'
		self.names = []
		self.urls = []
		self.nums = 0
		self.headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/71.0.3578.98 Safari/537.36' ,'Connection': 'close'}
		self.certFile = r'C:\Users\XuQ\Desktop\2.crt'
		
	def get_image_url(self, page):
		params = {
			'p':page,
			'type':'week',
			'data':'',
			}
		r = requests.get(self.url, params=params,headers=self.headers, verify=self.certFile)
		html = r.text
		soup = BeautifulSoup(html,'lxml')
		for a in soup.find_all('a',{'class':'db posr ovf'}):
			self.names.append(a['title'])
			self.urls.append(a.find('img')['src'])
			self.nums += 1
			
	def download(self, name, url):
		r = requests.get(url, headers=self.headers, verify=self.certFile)
		
		file_path = "E:/cos"
		if not os.path.exists(file_path):
			os.makedirs(file_path)
		os.chdir(file_path)
		
		path = name + url[-4:]
		with open(path, 'wb') as f:
			f.write(r.content)
			
def main(page):
	t = downloader()
	t.get_image_url(page)
	for i in range(t.nums):
		t.download(t.names[i],t.urls[i])

if __name__=="__main__":
	pool = Pool()

	pool.map(main, list(range(1,6)))
	pool.close()
	pool.join()
	
	

