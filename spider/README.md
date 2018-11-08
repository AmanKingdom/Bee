# WeChatDemo
### Debug 2.0

在spider.py的基础上更新了如下内容,并保存为spider2.0.py：  

  (1)html代码中所有的data-src替换为src  

	temp_html = requests.get(article_url)  
	temp_html.encoding = 'utf-8'  
	data = temp_html.text  
	html = re.sub(pattern='data-src', repl='src', string=data)  

  (2)增加了保存html代码到本地的代码，文件名为标题前10个字，处于注释状态，需要使用可删除注释。

	f = open('HTML/'+title[:10]+'.html', 'a+')
	f.write(html)
	f.close()

  (3)提取正文代码添加了异常处理  

	try:  
	    ps = content.find_all('p')  
	    for i in ps:  
	    	x = i.get_text()  
	    	# if '分享一篇文章' in x:       # 判断文章是否为分享其他文章的类型  
        	# return 'null'  
        	p_list.append(x)  

	    main_content = '\n'.join(p_list)
	except:  
	    return "null"                   #异常则返回null  

  (4)Test文件夹的文件为测试代码
  
---

### Debug 2.1

在spider2.0.py的基础上更新了如下内容，保存文件不变：   
  (1)增加了重复数据不插入数据库的代码，采用的方法是在原数据库的基础上关于publish_date,article_title建立唯一索引，建立了唯一索引后数据入库时会自动判断是否有重复数据：  

	def create_index():  
	    '''  
	    创建唯一索引  
	    :return:  
	    '''  
	    db = pymysql.connect(host='localhost', user='root', password='12345678', port=3306, db='spider')  
	    cursor = db.cursor()  
	    sql = 'CREATE UNIQUE INDEX unique_index ON wechat_article (publish_date,article_title)'  
	    cursor.execute(sql)  
	    db.close()  
	    log('unique_index索引已创建好')  
	    
  (2)优化了数据库操作的部分代码  
  
  (3)将老版本移至Older Version文件夹管理  
  
---  

### Debug 2.2  

1.在database.py的基础上更新如下内容，保存文件不变：  
更改了要创建的数据库为bee-database：

	cursor = db.cursor()
	cursor.execute("CREATE DATABASE bee_database DEFAULT CHARACTER SET UTF8MB4")
	db.close()

2.在spider2.0.py的基础上更新了如下内容，保存文件改为spider2.2.py：  
更改了原连接数据库spider为bee-database：  

	/#连接数据库
        self.db = pymysql.connect(host='localhost', user='root', password='12345678', port=3306, db='bee_database')
        self.cursor = self.db.cursor()

3.在search.py的基础上更新了如下内容，保存文件改为search2.2.py:

  (1)更改了原连接数据库spider为bee-database： 

	/# 连接数据库
        self.db = pymysql.connect(host='localhost', user='root', password='12345678', port=3306, db='bee_database')
        self.cursor = self.db.cursor()
	
  (2)将已分词的词语列表按照元素长度降序排序，如原列表：['北京','大学','北京大学','网易云','网易'] ，重新排序后变为：[‘北京大学','网易云','北京','大学','网易'] ，此举用于检索文章时优先检索长词，如果长词检索不到再检索短词，如果长词检索到了某一篇文章，那么该文章不再被短词检索。  

  (3)添加了同时检索文章标题和文章内容的代码，文章内容的检索是按行（p）检索  

  (4)返回数据增加了发布日期，公众号id，文章内容：  

	new_data = {
		'article_id' : data[0],
		'publish_date': data[3],
		'wechat_id': data[4],
		'article_title' : title,
		'article_content' : content
		}
		
---  

### Debug 2.3

1.增加了SQLite3数据库存储数据的版本，py文件存于WeChat_SQLite文件夹中  

2.spider2.2.py中增加了反防盗链的代码：

	html = re.sub(pattern='<head>', repl='<head><meta name="referrer" content="never">', string=html)

