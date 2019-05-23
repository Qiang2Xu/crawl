# crawl
A crawler beginner

## 初探python爬虫
### requests-BeautifulSoup
#### 静态网页
##### biqukan.py 用set类型去重，用dict存储小说名和URL。
##### biqukan_text.py 创建用于小说下载的类，
##### qula_text.py 方法和上一个相同，针对网页标签不同进行了修改
##### 动态网页
##### tadu_text.py 小说的内容有专门的URL存储，需要在从章节页面中提取
##### ajax_picture.py 下拉刷新图片，对ajax进行抓包，分析存放图片的网页URL规律，然后使用beautifulsoup提取图片的下载地址，使用多进程下载
##### ajax_stock.py ajax，抓取网页的存放数据的URL，得到json数据，多进程爬取
##### ajax_sina_gif.py ajax，抓取网页的存放gif图片相关信息的json数据，分析得到下载地址
