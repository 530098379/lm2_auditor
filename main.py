#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from pathlib import Path
import io
import sys
import re
import xlwt
import xlrd
import os
import time
import datetime

if __name__ == "__main__":
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
	print("开始", flush = True)
	add_flag = False #字符串拼接flag
	question_text = "" #输出字符串
	last_num = 0 #最后一次的工会编号
	last_year = datetime.datetime.now().year # 最后一次的年份，默认值为本年
	# 文件名
	excel_file_name = os.getcwd() + "\\result_" + \
		datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".xls"

	# 获取最后一次的工会编号以及年份
	my_file = Path("./the_last_dance.txt")
	if my_file.is_file():
		with open('./the_last_dance.txt', 'r') as f:
			last_data = (f.readline()).split(",")
			last_num = int(last_data[0])
			last_year = int(last_data[1])

	# 做成Excel文件
	count=0
	workbook = xlwt.Workbook()
	sheet = workbook.add_sheet("Sheet Name1")

	# 读取文件里面的工会代码
	excel_data = xlrd.open_workbook("lm2_auditor_input.xls")
	table = excel_data.sheet_by_index(0)
	del excel_data

	try:
		for rowNum in range(table.nrows):
			rowVale = table.row_values(rowNum)
			file_num = int(rowVale[0]) # 获取Excel第一列，工会代码

			# 如果当年工会编码小于最后一次的编码，则跳过去
			if file_num < last_num:
				continue

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
					if int(year) > last_year:
						continue

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
								question_text = question_text + k.next + " "
								add_flag = True
								continue

							if add_flag:
								if re.match("Question", k.next) or re.match("Schedule", k.next) \
									or re.match("Statement", k.next):
									print("工会编号:" + str(file_num), flush = True)
									print("年份:" + year, flush = True)
									print("内容:" + question_text, flush = True)
									print("--------------------------")
									sheet.write(count,0, file_num) # row, column, value
									sheet.write(count,1, year)
									sheet.write(count,2, question_text)
									count = count + 1;
									question_text = ""
									add_flag = False
								else:
									# 如果question12的内容是换行的，拼接数据
									question_text = question_text + k.next
						del k

					del r_detail
					del url_detail
					del param_detail
					del result_detail
					del bs_detail
					del data_detail
				# 延迟2秒，防止访问太快
				time.sleep(2)
				del j
				# 输出结果到Excel
				workbook.save(excel_file_name)

			# 释放变量内存
			del r_cok
			del url_cok

			del r_union		
			del url_union
			del param_union
			del result_union
			del bs_union
			del data_union

	finally:
		# 中断或者异常，记录最后的工会编码以及年份
		with open('./the_last_dance.txt', 'w') as obj_f:
			obj_f.write(str(file_num) + "," + year)

	# 执行完成后，删除文件
	if(os.path.exists('./the_last_dance.txt')):
		os.remove('./the_last_dance.txt')

	print("完成",flush = True)
