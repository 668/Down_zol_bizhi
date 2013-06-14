Down_zol_bizhi
==============

下载中关村壁纸站的壁纸图片

============================
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
如果有即提取出图片的地址
支持自定义分辨率  
