# 请求库
import requests
# 解析库
from bs4 import BeautifulSoup
# 用于解决爬取的数据格式化
import io
import sys

if __name__ == '__main__':
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
	# 爬取的网页链接
	url = 'https://olms.dol-esa.gov/query/getOrgQry.do'
	r =requests.get(url)
	# 类型
	# print(type(r))
	print(r.status_code)
	# 中文显示
	# r.encoding='utf-8'
	r.encoding=None
	
	cookie_jar = r.cookies

	url = 'https://olms.dol-esa.gov/query/orgReport.do'
	data = {'reportType':'detailResults','detailID':'1','detailReport':'unionDetail',
			'rptView':'undefined','historyCount':'0','screenName':'orgQueryResultsPage',
			'searchPage':'/getOrgQry.do','pageAction':'-1','startRow':'1',
			'endRow':'1','rowCount':'1','sortColumn':'','sortAscending':'false',
			'reportTypeSave':'orgResults'}
	r =requests.post(url, data, cookies=cookie_jar)
	print(r.status_code)
	result = r.text
	# 再次封装，获取具体标签内的内容
	bs = BeautifulSoup(result,'html.parser')
	# 获取已爬取内容中的td标签内容
	data1=bs.find_all('td')
	# 循环打印输出
	for j in data1:
		print(j.text)
