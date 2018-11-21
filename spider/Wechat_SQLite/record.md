# 爬虫模块的更新记录  

## 解决了图片下载到本地并且匹配到html中和删除右上角二维码的问题
 
> 图片下载到本地  

	在174和247行的 path_name = 'bee_imgs/' 设置存储路径  
	
	图片文件名为系统随机生成的30个字符串  
	
	html = re.sub(pattern='data-src=".*?"', repl='src="%s"' %img, string=html, count=1) 
	
	此行代码中的count=1 表示每次只替换1个，而不是全部都替换
	  
	  
> 二维码问题 
  
	二维码删除问题采用re.sub替换的方法  
	
	其中的delete变量的内容为匹配字段，不可更改缩进，否则匹配不到
  
  

>数据库重复问题

	此前的判断数据重复的方法是在爬取一篇文章的所有信息之后  
	
	而加入下载图片的代码后使爬取工作量变大  
	
	因此此后在爬取一篇文章的所有信息之前就做重复判断  
	
	判断方法是查询当前文章标题与发布时间是否存在数据库中
	
	if len(exits) >= 1:
		Spider.log("%s", '数据已存在，忽略此次爬取.')
		continue

## 2018-11-21 修复了图片错乱的bug和增加了视频显示的功能

> 分析    
    
    观察图片的url，可见大部分图片以文件类型（png/jpeg/gif）结尾，
    
    而结尾没有文件类型的是以https://mmbiz.qpic.cn/mmbiz_jpg _png _gif开头,
    
    虽然也存在以https://mmbiz.qpic.cn/mmbiz和https://res.wx.qq.com开头的，
    
    但此类会有文件类型结尾，而视频则以https://v.qq.com/iframe开头，
    
    分析完后便可进行设计爬虫代码。
    
    生成随机字符串作为图片文件名，先利用endswith判断文件类型，
    
    无法判断时再利用startswith（）判断文件类型，图片文件名存入列表，
    
    如果是视频，则存入‘video’以为下一步判断视频类型做准备。
    
> 在处理HTML代码时，判断如果有视频内容，即替换data-src为src即可：

    for img_name in imgs:                 # 依次将data-src替换为本地路径
        if img_name == 'video':
            html = re.sub(pattern='data-src', repl='src', string=html, count=1)
        else:
            img = path_name+img_name
            html = re.sub(pattern='data-src=".*?"', repl='src="%s"' %img, string=html, count=1)