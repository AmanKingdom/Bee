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