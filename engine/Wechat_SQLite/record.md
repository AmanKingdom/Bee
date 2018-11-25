# 爬虫模块的更新记录  

## 2018-11-16 解决了图片下载到本地并且匹配到html中和删除右上角二维码的问题
 
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
    
> 在处理HTML代码时，判断如果有视频内容，则替换data-src为src即可：

    for img_name in imgs:                 # 依次将data-src替换为本地路径
        if img_name == 'video':
            html = re.sub(pattern='data-src', repl='src', string=html, count=1)
        else:
            img = path_name+img_name
            html = re.sub(pattern='data-src=".*?"', repl='src="%s"' %img, string=html, count=1)
            
## 2018-11-22 历史文章爬取顺序改为先旧后新

> 将列表反转

    items = []
    for item in articles_list.items():
        items.append(item)
    items.reverse()
    
## 2018-11-23 删除数据库冗余数据项、增加其他数据项和增加公众号表

> 删除项

    article_img     # 文章图片 
    
> 增加项

    img_amount        # 文章图片数量
    word_amount       # 文章文字数量
    video_amount      # 文章视频数量
    audio_amount      # 文章音频数量
    
## 2018-11-24（1） 增加了爬取公众号信息的爬虫

> 代码位置

    spider.Wechat_SQLite.spider_sqlite.AccountSpider

> 功能说明

    通过传入公众号微信号（wechat_id），
    利用selenium自动化获取公众号的url，
    进而通过pyquery解释页面获取公众号名称、头像url，
    
    头像下载到本地的../../static/head_portraits/文件夹
    头像文件命名为长度30的随机字符串，文件类型为png
    如：dWtKGuEa0V5OsQkIzgvCb6T3SBD9Rr.png
    
> 数据库说明

    每个公众号爬取之前都会先进行查询数据库是否存在此条记录
    如存在则不会调用selenium，节省系统资源
    
    每个公众号的信息只有在入库成功才会下载头像文件
    避免下载了文件而入库不成功造成资源浪费
    
## 2018-11-24（2） 增加了请求超时异常处理和日志保存到本地文件功能

> 请求超时异常处理

    所有的requests请求都加入了超时异常处理
    可以解决爬虫进行过程中因网络环境的变动而卡住的问题
    如：
    try:
        search_html = self.session.get(search_url,headers=self.headers, timeout=self.timeout).content

    except:
        Log.article_log('请求超时，将爬取下一个公众号。')
        continue
        
    try:
        data = requests.get(img, headers=self.headers, timeout=self.img_timeout)
    except:
        return 'timeout'
        
> 日志保存到本地文件

    日志文件分为文章爬虫：article_log，公众号爬虫：account_log
    
    class Log:

    def article_log(msg):
        '''
        日志函数
        :param msg: 日志信息
        :return:
        '''
        f = open('../LogFile/article_log.log', 'a+')
        print(u'%s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg))
        f.write(u'%s: %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg))
        f.close()

    def account_log(msg):
        '''
        日志函数
        :param msg: 日志信息
        :return:
        '''
        f = open('../LogFile/account_log.log', 'a+')
        print(u'%s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg))
        f.write(u'%s: %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg))
        f.close()
        
## 2018-11-25 增加了下载文章封面图到本地的功能

> 说明
    
    封面图片文件名为系统随机生成的30个字符串
    文件存储于../../static/cover_imgs/文件夹
    入库的数据由图片url改为图片名称（不带路径名）
    
    path_cover = '../../static/cover_imgs/'
    ran_str = (''.join(random.sample(string.ascii_letters + string.digits, 30)))
    cover_name = ran_str + '.jpeg'

    try:
        cover_data = requests.get(pic, headers=self.headers, timeout=self.img_timeout)
    except:
        Log.article_log('封面图请求超时，将爬取下一篇文章。')
        continue
    fp = open(path_cover + cover_name, 'wb')  # 下载图片到本地
    fp.write(cover_data.content)
    fp.close()