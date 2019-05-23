import requests, sys, os, json
from jsonpath import jsonpath
from bs4 import BeautifulSoup
from multiprocessing.pool import Pool

url = 'http://query.sse.com.cn/security/stock/getStockListData2.do?'

def main(page):
	params = {
		'jsonCallBack':'jsonpCallback71218',
		'isPagination':'true',
		'stockCode':'',
		'csrcCode':'',
		'areaName':'',
		'stockType':1,
		'pageHelp.cacheSize':1,
		'pageHelp.beginPage':page,
		'pageHelp.pageSize':25,
		'pageHelp.pageNo':page,
		'pageHelp.endPage':1 + page*10,
		}

	headers={'Cookie':'yfx_c_g_u_id_10000042=_ck18012900250116338392357618947; VISITED_MENU=%5B%228528%22%5D; yfx_f_l_v_t_10000042=f_t_1517156701630__r_t_1517314287296__v_t_1517320502571__r_c_2',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
	'Referer':'http://www.sse.com.cn/assortment/stock/list/share/'
	}

	r = requests.get(url, params=params, headers=headers)
	json_str = '{"content":' + r.text[19:-1] + '}'
	print(json_str)
	unicode_str = json.loads(json_str)

	COMPANY_CODE=jsonpath(unicode_str,'$..pageHelp..COMPANY_CODE')#公司/A股代码
	COMPANY_ABBR=jsonpath(unicode_str,'$..pageHelp..COMPANY_ABBR')#公司/A股简称
	totalShares=jsonpath(unicode_str,"$..pageHelp..totalShares") #A股总资本
	totalFlowShares=jsonpath(unicode_str,'$..pageHelp..totalFlowShares') #A股流动资本

	
	for i in range(len(COMPANY_CODE)):
		print(COMPANY_CODE[i],'\t','\t',COMPANY_ABBR[i],'\t','\t',totalShares[i],'\t','\t',totalFlowShares[i])

if __name__ == '__main__':
	print('公司/A股代码','\t','公司/A股简称','\t','A股总资本','\t','A股流动资本')
	pages = list(range(1,31))
	pool = Pool()
	pool.map(main, pages)
	pool.close()
	pool.join()































