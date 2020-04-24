#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import io
import sys
import re
import xlwt
import xlrd
import os
import time

if __name__ == "__main__":
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
	print("开始", flush = True)

	# 做成Excel文件
	count=0
	workbook = xlwt.Workbook()
	sheet = workbook.add_sheet("Sheet Name1")

	# 读取文件里面的工会代码
	excel_data = xlrd.open_workbook("lm2_auditor2.xls")
	table = excel_data.sheet_by_index(0)
	del excel_data

	for rowNum in range(table.nrows):
		rowVale = table.row_values(rowNum)
		file_num = int(rowVale[0]) # 获取Excel第一列，工会代码

		# 获取cookie
		url_cok = "https://olms.dol-esa.gov/query/getOrgQry.do"
		r_cok =requests.get(url_cok)
		cookie_jar = r_cok.cookies

		# 获取当前工会的所有年报
		url_union = "https://olms.dol-esa.gov/query/orgReport.do"
		param_union = {"reportType":"detailResults","detailID":file_num,"detailReport":"unionDetail",
				"rptView":"undefined","historyCount":"0","screenName":"orgQueryResultsPage",
				"searchPage":"/getOrgQry.do","pageAction":"-1","startRow":"1",
				"endRow":"1","rowCount":"1","sortColumn":"","sortAscending":"false",
				"reportTypeSave":"orgResults"}
		r_union =requests.post(url_union, param_union, cookies=cookie_jar)
		#print(r.status_code)

		# 再次封装，获取具体标签内的内容
		result_union = r_union.text
		bs_union = BeautifulSoup(result_union,"html.parser")

		# 获取已爬取内容中的Fiscal Year行的链接
		data_union = bs_union.select("a[class='getFormReportLink']")

		# 循环打印输出
		for j in data_union:
			year = (j.text)[0:4]
			# 获取的链接，年份大于2005，并且是报告的时候，打开链接
			if year.isdigit() and int(year) > 2005 and (j.text).find("Report") >= 0:
				strlist = j["href"].split(",") # 获取年报的编码

				# 获取当前工会的Question 12
				url_detail = "https://olms.dol-esa.gov/query/orgReport.do"
				param_detail = {"reportType":"formReport","detailID":strlist[1],"detailReport":"LM2Form",
						"rptView":"undefined","historyCount":"1","screenName":"orgDetailPage",
						"searchPage":"/getOrgQry.do","pageAction":"-1","startRow":"1",
						"endRow":"25","rowCount":"25","sortColumn":"","sortAscending":"false",
						"reportTypeSave":"detailResults"}
				r_detail =requests.post(url_detail, param_detail, cookies=cookie_jar)
				#print(r.status_code)

				# 再次封装，获取具体标签内的内容
				result_detail = r_detail.text
				bs_detail = BeautifulSoup(result_detail,"html.parser")

				# 获取已爬取内容中的Fiscal Year行的链接
				data_detail = bs_detail.select("div[class='ERDS-form-text'] br")

				# 循环打印输出
				for k in data_detail:
					# 判断下一个元素是字符串
					if isinstance(k.next, str):
						if re.match("Question\s12", k.next):
							print("工会编号:" + str(file_num), flush = True)
							print("年份:" + year, flush = True)
							print("内容:" + k.next, flush = True)
							print("--------------------------")
							sheet.write(count,0, file_num) # row, column, value
							sheet.write(count,1, year)
							sheet.write(count,2, k.next)
							count = count + 1;
					del k
			# 延迟5秒，防止访问太快
			time.sleep(5)
			del j
		# 释放变量内存
		del r_cok
		del url_cok

		del r_union		
		del url_union
		del param_union
		del result_union
		del bs_union
		del data_union

		del r_detail
		del url_detail
		del param_detail
		del result_detail
		del bs_detail
		del data_detail
	# 输出结果到Excel
	workbook.save(os.getcwd() + "/result.xls")
	print("完成",flush = True)
