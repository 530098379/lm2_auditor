import requests
from bs4 import BeautifulSoup
import io
import sys
import re
import xlwt
import xlrd
import os

if __name__ == '__main__':
	excel_data = xlrd.open_workbook("lm2_auditor2.xls")
	table = excel_data.sheet_by_index(0)

	for rowNum in range(table.nrows):
		rowVale = table.row_values(rowNum)
		for colNum in range(table.ncols):
			if rowNum > 0 and colNum == 0:
				print(int(rowVale[0]))
			else:
				print(rowVale[colNum])
		print("---------------")

	sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
	# 获取cookie
	url = 'https://olms.dol-esa.gov/query/getOrgQry.do'
	r =requests.get(url)
	cookie_jar = r.cookies

	# 获取当前工会的所有年报
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
	# 获取已爬取内容中的Fiscal Year行的链接
	data1=bs.select('a[class="getFormReportLink"]')
	# 循环打印输出
	#for j in data1:
		#print(j['href'])

	# 获取当前工会的Question 12
	url = 'https://olms.dol-esa.gov/query/orgReport.do'
	data = {'reportType':'formReport','detailID':'707004','detailReport':'LM2Form',
			'rptView':'undefined','historyCount':'1','screenName':'orgDetailPage',
			'searchPage':'/getOrgQry.do','pageAction':'-1','startRow':'1',
			'endRow':'25','rowCount':'25','sortColumn':'','sortAscending':'false',
			'reportTypeSave':'detailResults'}
	r =requests.post(url, data, cookies=cookie_jar)
	print(r.status_code)

	result = r.text
	# 再次封装，获取具体标签内的内容
	bs = BeautifulSoup(result,'html.parser')
	# 获取已爬取内容中的Fiscal Year行的链接
	data1=bs.select('div[class="ERDS-form-text"] br')

	count=0
	workbook = xlwt.Workbook()
	sheet = workbook.add_sheet("Sheet Name1")
	# 循环打印输出
	for j in data1:
		# 判断下一个元素是字符串
		if isinstance(j.next, str):
			if re.match("Question\s12", j.next):
				print(j.next)
				sheet.write(count,0, "1") # row, column, value
				sheet.write(count,1, "2019")
				sheet.write(count,2, j.next)
	workbook.save(os.getcwd() + '/result.xls')
