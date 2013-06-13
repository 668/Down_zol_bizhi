#!/usr/bin/env python
#!encoding:utf-8
#!filename:Down_zol_bizhi.py

"""
Copyright 2013 Dwon_zol_bizhi
====
下载中关村壁纸站的JPG格式的壁纸

author    	=	"Sam Huang"
name    		=	"Down_zol_bizhi"
version 		=   "1.0.1"
url 			=	"http://www.hiadmin.org"
author_email	=	"sam.hxq@gmail.com"


@zol_url_list(zol_url)函数 
接收一个url列表页面、然后分析提取url里面的分类壁纸地址并
写入到一个zol_bizhi_url_list列表对象中
http://desk.zol.com.cn/pc/hot_1.html 下载量排序
http://desk.zol.com.cn/pc/good_1.html 推荐数排序
http://desk.zol.com.cn/pc/1.html            最新更新排序

@zol_page_nex(url)         
接收一个分类的壁纸地址，然后提取出本分类中下一张地址赋值给page_next
及本分类的名称zol_bizhi_name(用于在本地创建文件夹存放本分类图片文件)

down_zol_jpg(url,resolution="1920x1080")：
接收一个图片url地址和一个壁纸分辨率大小、然后分析传入的url中是否有此分辨率大小的图片
如果有即提取出图片的此。
支持1920x1200/1920x1080/1680x1050/1600x900/1440x90/1366x768/1280x1024分辨率  
"""

import re
import requests
import os

def zol_url_list(zol_url):
    """分析传入的url、吧里面的分类壁纸地址提取出来、然后写入列表中
    @zol_url        	:中关村壁纸分类地址
    @zol_bizhi_url_list :用re.findall吧分类里面的壁纸列表分组地址提取出来保    
                        存到列表中
    @urlList_reg    	:用于提取分类壁纸列表分组的正则表达式
    """
    r = requests.get(zol_url)
    zol_txt = r.text
    urlList_reg = r"(<li class=\"photo-list-padding\"><a class=\"pic\" href=)\"(/bizhi/\d+_\d+_\d+.html)"
    zol_bizhi_list_temp = re.findall(urlList_reg,zol_txt)
    #吧re.findall返回的列表内容提取之后写入到zol_bizhi_url_list中
    global zol_bizhi_url_list
    zol_bizhi_url_list = []
    list_temp = []
    for i in zol_bizhi_list_temp:
    	#将findall返回列表中的值提取出来append到list_temp中
        list_temp.append("http://desk.zol.com.cn"+i[1])

    zol_bizhi_url_list = list_temp


def zol_page_next(url):
	"""根据传入的图片地址来提取本分组里面下一张壁纸地址
	@zol_name_reg	:用于提取<h3>里面的描述，用于作为本地存放图片的文件夹
	@page_next_reg	:用于在本图片页面提取下一张图片的地址
	@zol_bizhi_name	:图片分组名称，用于在本地建立文件夹来存放此分组的图片
	@page_next 		:提取分析之后的本组图片的下一张图片地址
	"""
	zol_name_reg = r"(<h3>.*>)(.*)(</a><span>)"
	page_next_reg = r"(id=\"pageNext\".*href=\")(/bizhi/\d+_\d+_\d+.html)\"\s(title=\"点击浏览下一张)"
	r = requests.get(url)
	if r.status_code == 200:
		r_txt = r.text
		global zol_bizhi_name
        #判断是否能找到图片分类名称
		if re.search(zol_name_reg,r_txt) !=None:
			zol_bizhi_name = re.search(zol_name_reg,r_txt).group(2) 
		#如果正则表达式返回不为None就认为匹配成功
		if re.search(page_next_reg,r_txt).group() != None:
			page_next_temp = re.search(page_next_reg,r_txt).group(2)
			global page_next
			page_next = "http://desk.zol.com.cn%s"%page_next_temp
			print ("PageNext: ",page_next)
			print ()
		else:
			print (".....已经没下一页.....")




def down_zol_jpg(url,resolution="1920x1080"):
	"""下载指定页面指定分辨率的壁纸
	指定2个参数，url用于接收壁纸地址页面
	resolution用于指定分辨率参数，默认值为1920x1080、
    支持1920x1200/1920x1080/1680x1050/1600x900/1440x90/1366x768/1280x1024分辨率
	@reg_xxx		:提取指定大小的分辨率的页面地址
	@zol_jpg_reg	:提取图片地址和图片名称的
	@down_url 		:指定分辨率戴奥的壁纸页面
	@zol_jpg_url	:壁纸下载url
	@zol_jpg_name   :用于本地存储的图片名称
	@zol_bizhi_name	:壁纸名称，也就是本地用于存放壁纸的文件夹
	"""
	#()匹配以id=这样开头以href="结尾的，第二个()匹配以/showpic开头以.html结尾
	#匹配完成之后我们用.group(2)来提取需要的第二个()里面的内容
	reg_1920x1200 = "(id=\"1920x1200\" href=\")(/showpic/\d+x\d+_\d+_\d+.html)"
	reg_1920x1080 = "(id=\"1920x1080\" href=\")(/showpic/\d+x\d+_\d+_\d+.html)"
	reg_1680x1050 = "(id=\"1680x1050\" href=\")(/showpic/\d+x\d+_\d+_\d+.html)"
	reg_1600x900 = "(id=\"1600x900\" href=\")(/showpic/\d+x\d+_\d+_\d+.html)"
	reg_1440x900 = "(id=\"1440x900\" href=\")(/showpic/\d+x\d+_\d+_\d+.html)"
	reg_1366x768 = "(id=\"1366x768\" href=\")(/showpic/\d+x\d+_\d+_\d+.html)"
	reg_1280x1024 = "(id=\"1280x1024\" href=\")(/showpic/\d+x\d+_\d+_\d+.html)"
	#用二个()吧正则表达式分开,当使用group()的时候就是完整的url地址
	#使用group(2)的就是提取.jpg，吧这个用来作为本地存储图片的文件名称
	zol_jpg_reg = "(http://.*/)(\d+.jpg)"

	r1 = requests.get(url)
	if r1.status_code ==200: #如果状态码为200说明页面能正常访问
		r1_txt = r1.text
		if resolution == "1920x1200":#根据传入数据来判断提取什么分辨率的壁纸
			if re.search(reg_1920x1200,r1_txt) != None:
			#判断本张图片是否有此分辨率大小
			
				down_url_temp = re.search(reg_1920x1200,r1_txt).group(2)
				down_url = "http://desk.zol.com.cn%s"%down_url_temp
				print ("PageUrl: ",down_url)

				r2 = requests.get(down_url)
				"""
				通过上面提取到的图片html地址，再次提取单张图片的url地址
				以及单张url的文件名称
				然后用requests模块的.content去吧图片写入到文件
				"""
				if r2.status_code == 200:
					r2_txt = r2.text
					if re.search(zol_jpg_reg,r2_txt) != None:
						zol_jpg_url = re.search(zol_jpg_reg,r2_txt).group() #jpg图片的URL地址
						zol_jpg_name = re.search(zol_jpg_reg,r2_txt).group(2) #JPG图片的名称
						print ("JpgUrl: ",zol_jpg_url)
						url_jpg = requests.get(zol_jpg_url)
						if url_jpg.status_code == 200: 
						#如果能正常打开图片的url就开始下载
						#用requests的.content功能吧图片写入到本地
							with open("%s/%s"%(zol_bizhi_name,zol_jpg_name),"wb") as code:
								code.write(url_jpg.content)

		#下面的6个条件判断主要用于判断用户要下载的壁纸分辨率
		#其他代码和上面的一样

		elif resolution == "1920x1080":
			if re.search(reg_1920x1080,r1_txt) != None:
				down_url_temp = re.search(reg_1920x1080,r1_txt).group(2)
				down_url = "http://desk.zol.com.cn%s"%down_url_temp
				print ("PageUrl: ",down_url)
				r2 = requests.get(down_url)
				if r2.status_code == 200:
					r2_txt = r2.text
					if re.search(zol_jpg_reg,r2_txt) != None:
						zol_jpg_url = re.search(zol_jpg_reg,r2_txt).group()
						zol_jpg_name = re.search(zol_jpg_reg,r2_txt).group(2)
						print ("JpgUrl: ",zol_jpg_url)
						url_jpg = requests.get(zol_jpg_url)
						if url_jpg.status_code == 200:
							with open("%s/%s"%(zol_bizhi_name,zol_jpg_name),"wb") as code:
								code.write(url_jpg.content)


		elif resolution == "1680x1050":
			if re.search(reg_1680x1050,r1_txt) != None:
				down_url_temp = re.search(reg_1680x1050,r1_txt).group(2)
				down_url = "http://desk.zol.com.cn%s"%down_url_temp
				print ("PageUrl: ",down_url)
				r2 = requests.get(down_url)
				if r2.status_code == 200:
					r2_txt = r2.text
					if re.search(zol_jpg_reg,r2_txt) != None:
						zol_jpg_url = re.search(zol_jpg_reg,r2_txt).group()
						zol_jpg_name = re.search(zol_jpg_reg,r2_txt).group(2)
						print ("JpgUrl: ",zol_jpg_url)
						url_jpg = requests.get(zol_jpg_url)
						if url_jpg.status_code == 200:
							with open("%s/%s"%(zol_bizhi_name,zol_jpg_name),"wb") as code:
								code.write(url_jpg.content)

		elif resolution == "1600x900":
			if re.search(reg_1600x900,r1_txt) !=None:
					down_url_temp = re.search(reg_1600x900,r1_txt).group(2)
					down_url = "http://desk.zol.com.cn%s"%down_url_temp
					print ("PageUrl: ",down_url)
					r2 = requests.get(down_url)
					if r2.status_code == 200:
						r2_txt = r2.text
						if re.search(zol_jpg_reg,r2_txt) !=None:
							zol_jpg_url = re.search(zol_jpg_reg,r2_txt).group()
							zol_jpg_name = re.search(zol_jpg_reg,r2_txt).group(2)
							print ("JpgUrl: ",zol_jpg_url)
							url_jpg = requests.get(zol_jpg_url)
							if url_jpg.status_code == 200:
								with open("%s/%s"%(zol_bizhi_name,zol_jpg_name),"wb") as code:
									code.write(url_jpg.content)


		elif resolution == "1440x900":
			if re.search(reg_1440x900,r1_txt) !=None:
				down_url_temp = re.search(reg_1440x900,r1_txt).group(2)
				down_url = "http://desk.zol.com.cn%s"%down_url_temp
				print ("PageUrl: ",down_url)
				r2 = requests.get(down_url)
				if r2.status_code == 200:
					r2_txt = r2.text
					if re.search(zol_jpg_reg,r2_txt)!=None:
						zol_jpg_url = re.search(zol_jpg_reg,r2_txt).group()
						zol_jpg_name = re.search(zol_jpg_reg,r2_txt).group(2)
						print ("JpgUrl: ",zol_jpg_url)
						url_jpg = requests.get(zol_jpg_url)
						if url_jpg.status_code == 200:
							with open("%s/%s"%(zol_bizhi_name,zol_jpg_name),"wb") as code:
								code.write(url_jpg.content)


		elif resolution == "1366x768":
			if re.search(reg_1366x768,r1_txt) !=None:
				down_url_temp = re.search(reg_1366x768,r1_txt).group(2)
				down_url = "http://desk.zol.com.cn%s"%down_url_temp
				print ("PageUrl: ",down_url)
				r2 = requests.get(down_url)
				if r2.status_code == 200:
					r2_txt = r2.text
					if re.search(zol_jpg_reg,r2_txt) !=None:
						zol_jpg_url = re.search(zol_jpg_reg,r2_txt).group()
						zol_jpg_name = re.search(zol_jpg_reg,r2_txt).group(2)
						print ("JpgUrl: ",zol_jpg_url)
						url_jpg = requests.get(zol_jpg_url)
						if url_jpg.status_code == 200:
							with open("%s/%s"%(zol_bizhi_name,zol_jpg_name),"wb") as code:
								code.write(url_jpg.content)


		elif resolution == "1280x1024":
			if re.search(reg_1280x1024,r1_txt) !=None:
				down_url_temp = re.search(reg_1280x1024,r1_txt).group(2)
				down_url = "http://desk.zol.com.cn%s"%down_url_temp
				print ("PageUrl: ",down_url)
				r2 = requests.get(down_url)
				if r2.status_code == 200:
					r2_txt = r2.text
					if re.search(zol_jpg_reg,r2_txt) !=None:						
						zol_jpg_url = re.search(zol_jpg_reg,r2_txt).group()
						zol_jpg_name = re.search(zol_jpg_reg,r2_txt).group(2)
						print ("JpgUrl: ",zol_jpg_url)
						url_jpg = requests.get(zol_jpg_url)
						if url_jpg.status_code == 200:
							with open("%s/%s"%(zol_bizhi_name,zol_jpg_name),"wb") as code:
								code.write(url_jpg.content)
		else:
			print ("没有这个分辨率，请重新设置分辨率。")
			print (".....NO is resolution...")




if __name__ == "__main__":
	url_list = [] 
	item_list = [] 
	"""
	url_list = [] 用于存放单个分类里面的所有图片地址、以便于确认是否已经下载完成
	item_list = [] 用于存放分类图片地址、zol_bizhi_url_list的数据将写入此列表中
	range(1,10),从第一页开始到第十页结束，并将zol_url_list函数返回的列表内容写入到item_list中
	"""
	for i in range(1,10):
		url = "http://desk.zol.com.cn/pc/hot_%s.html"%i
		zol_url_list(url)
		for x in zol_bizhi_url_list:			
			item_list.append(x)
	print (len(item_list))


	for jpg_url in item_list:
		"""
		将遍历item_list列表，将其作为zol_page_next函数的值传入
		用zol_page_next函数中zol_bizhi_name变量返回值来创建本地文件夹
		用于存放单个分类里面图片。


		"""
		while True:
			zol_page_next(jpg_url)
			#将函数zol_page_next返回的值写入到list中,并用len()和len(set())进行判断是否相等
			#如果不相等即说明list中有重复值，即本分组的图片地址已经全部提取出来。
			if len(url_list) == len(set(url_list)):
				#判断本地是否已经存在此文件夹，如果不存在就创建此文件夹
				if os.path.exists("%s"%zol_bizhi_name) == False:
					zol_bizhi_name = os.mkdir("%s"%zol_bizhi_name)

				elif os.path.exists("%s"%zol_bizhi_name) == True:
					url_list.append(page_next)
					jpg_url = page_next
					down_zol_jpg(page_next,resolution="1920x1080")
				#continue
			else:
				url_list = [] #将列表初始化为空
				break
	


			

