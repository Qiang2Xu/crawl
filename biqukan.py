import requests
from bs4 import BeautifulSoup
from urllib.requests import urljoin

class Title(object):

	def __init__(self):
		self.server = "https://www.biqukan.com/"
		self.page_url = set()
		self.title_url = dict()
        
	def get_page_url(self):
		r = requests.get(self.server)
		soup = BeautifulSoup(r.text,'lxml')
		for li in soup.select("div.nav > ul > li")[2:-2]:
			href = li.a['href']
			url = urljoin(self.server, href)
			self.page_url.add(url)
            
	def get_title_url(self, url):
		r = requests.get(url)
		soup = BeautifulSoup(r.text, 'lxml')
		wrap = soup.select_one('body > div.wrap')

		
		for i in wrap.find_all('div', class_='p10'):
			href = i.find('dl').a['href']
			name = i.find('dl').a.text
			url = urljoin(self.server, href)
			self.title_url[name] = url
		
		for span in wrap.find_all('span', class_='s2'):
			href = span.a['href']
			name = span.a.text
			url = urljoin(self.server, href)
			self.title_url[name] = url
			
if __name__ == "__main__":
	t1 = Title()
	t1.get_page_url()
	for url in t1.page_url:
		t1.get_title_url(url)
	path = "E:/笔趣看小说.txt"
	with open(path, 'w') as f:
		for name, url in t1.title_url.items():
			f.write(name+'\t'+url+'\n')
