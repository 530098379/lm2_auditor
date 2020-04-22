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
	r= requests.get("https://olms.dol-esa.gov/query/getOrgQry.do")
	# 类型
	# print(type(r))
	print(r.status_code)
	# 中文显示
	# r.encoding='utf-8'
	r.encoding=None
	print(r.encoding)
	print(r.text)
	result = r.text
	# 再次封装，获取具体标签内的内容
	bs = BeautifulSoup(result,'html.parser')
	# 具体标签
	print("解析后的数据")
	print(bs.span)
	a={}
	# 获取已爬取内容中的script标签内容
	data=bs.find_all('script')
	# 获取已爬取内容中的td标签内容
	data1=bs.find_all('td')
	# 循环打印输出
	for i in data:
		a=i.text
		print(i.text,end='')
		for j in data1:
			print(j.text)