# Python_WeChatDemo
**Debug 2.0**

在spider.py的基础上更新了如下内容：  

1.html代码中所有的data-src替换为src  

	temp_html = requests.get(article_url)  
	temp_html.encoding = 'utf-8'  
	data = temp_html.text  
	html = re.sub(pattern='data-src', repl='src', string=data)  

2.增加了保存html代码到本地的代码，文件名为标题前10个字，处于注释状态，需要使用可删除注释。

	f = open('HTML/'+title[:10]+'.html', 'a+')
	f.write(html)
	f.close()

3.提取正文代码添加了异常处理  

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

4.Test文件夹的文件为测试代码
