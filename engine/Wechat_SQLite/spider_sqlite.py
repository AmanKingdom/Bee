# coding: utf-8
import random
import re
import os
import string
import time
import sqlite3
import pymysql
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from pyquery import PyQuery as pq

class Log:

    def article_log(msg):
        '''
        日志函数
        :param msg: 日志信息
        :return:
        '''
        # f = open('../LogFile/article_log.log', 'a+')
        f = open('engine/LogFile/article_log.log', 'a+')
        print(u'%s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg))
        f.write(u'%s: %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg))
        f.close()

    def account_log(msg):
        '''
        日志函数
        :param msg: 日志信息
        :return:
        '''
        # f = open('../LogFile/account_log.log', 'a+')
        f = open('engine/LogFile/account_log.log', 'a+')
        print(u'%s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg))
        f.write(u'%s: %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg))
        f.close()

class ArticleSpider:
    '''
    文章爬虫，用于爬取微信文章的各项信息
    '''

    def __init__(self, wechat_ids):
        '''
        构造函数，根据公众号微信号获取对应文章的发布时间、文章标题, 文章链接等信息
        :param
        '''
        self.wechat_ids = wechat_ids

        # 请求头
        self.headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

        # 超时时长
        self.timeout = 5

        # 图片爬取超时时长
        self.img_timeout = 10

        # 爬虫模拟在一个request.session中完成
        self.session = requests.Session()

        # 连接数据库
        self.db = sqlite3.connect('../../bee-database.db')
        self.cursor = self.db.cursor()


    def get_infos(self):

        Log.article_log('正在爬取文章信息。。。')
        for wechat_id in self.wechat_ids:

            print('\n')
            Log.article_log(u'公众号ID为：%s' % wechat_id)

            # 搜索url
            search_url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query=' + wechat_id
            try:
                search_html = self.session.get(search_url,headers=self.headers, timeout=self.timeout).content

            except:
                Log.article_log('请求超时，将爬取下一个公众号。')
                continue

            #获取公众号URL
            doc = pq(search_html)
            wechat_url = doc('div[class=txt-box]')('p[class=tit]')('a').attr('href')
            if wechat_url == None:
                Log.article_log('未知错误，将爬取下一个公众号。')
                continue
            wechat_name = doc('#sogou_vr_11002301_box_0 .txt-box a').text().strip()
            Log.article_log(u'公众号名称：%s' % wechat_name)
            Log.article_log(u'公众号url：%s' % wechat_url)

            # 获取html
            browser = webdriver.Chrome()
            browser.get(wechat_url)
            time.sleep(2)
            wechat_html = browser.execute_script("return document.documentElement.outerHTML")
            browser.close()

            # 检测是否被限制访问
            if pq(wechat_html)('#verify_change').text() != '':
                Log.article_log(u'已限制访问，请稍后再试')

            else:
                # 获取发布时间，标题，首图，URL
                doc = pq(wechat_html)
                articles_list = doc('div[class="weui_media_box appmsg"]')
                articlesLength = len(articles_list)
                Log.article_log(u'抓到文章%s篇' % articlesLength)

                items = []
                for item in articles_list.items():
                    items.append(item)
                items.reverse()

                if articles_list:
                    index = 1

                    for article in items:

                        Log.article_log('')
                        Log.article_log('正在爬取(%s/%s)' % (index, articlesLength))
                        index += 1

                        # 获取标题
                        title = article('h4[class="weui_media_title"]').text().strip()
                        Log.article_log(u'标题： %s' % title)

                        # 获取文章发表时间
                        temp_date = article('p[class="weui_media_extra_info"]').text().strip()
                        if temp_date.endswith("原创"):
                            pdate = temp_date.replace('原创','')
                        else:
                            pdate = temp_date
                        Log.article_log(u'发表时间： %s' % pdate)

                        # 获取标题对应的地址
                        temp_url = article('h4[class="weui_media_title"]').attr('hrefs')
                        # 存在某些推文的临时链接为完整链接，判断是否需要拼接
                        if temp_url.startswith('http://mp.weixin.qq.com'):
                            article_url = temp_url
                        else:
                            article_url = 'http://mp.weixin.qq.com' + temp_url
                        Log.article_log(u'地址： %s' % article_url)

                        # 在获取到标题和发布日期的时候先进行查询数据库是否存在此条记录
                        sql1 = "SELECT article_title, publish_date FROM wechat_article WHERE article_title='" + title + "'"+"AND publish_date='"+pdate+"'"
                        self.cursor.execute(sql1)
                        exits = self.cursor.fetchall()  # 查找所有符合条件的数据
                        if len(exits) >= 1:
                            Log.article_log('数据已存在，忽略此次爬取.')
                            continue

                        # 获取封面图片
                        cover = article('.weui_media_hd').attr('style')

                        pic = re.compile(r'background-image:url(.+)')
                        rs = pic.findall(cover)
                        if len(rs) > 0:
                            pic = rs[0].replace('(', '')
                            pic = pic.replace(')', '')
                            #self.log(u'封面图片：%s ' % pic)

                        # 下载封面图到本地
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

                        # 获取正文内容
                        if title == "分享图片":     # 判断文章是否是为分享图片的类型
                            content = "null"
                        else:
                            content = self.get_atticle_info(article_url)

                        if content == 'timeout':
                            Log.article_log('请求文章内容超时，将爬取下一篇文章。')
                            continue

                        # 获取文章图片
                        imgs = self.get_article_img(article_url)
                        if imgs == 'timeout':
                            Log.article_log('下载图片超时，将爬取下一篇文章。')
                            continue

                        # 从数据库获取公众号二维码图片
                        sql2 = "SELECT qr_code FROM wechat_account WHERE wechat_id='" + wechat_id + "'"
                        self.cursor.execute(sql2)
                        qr_code = self.cursor.fetchone()[0]  # 查找符合条件的数据
                        qr_code_path = '../../static/qr_codes/' + qr_code

                        # 获取html代码
                        try:
                            temp_html = requests.get(article_url, headers=self.headers, timeout=self.timeout)
                        except:
                            Log.article_log('html代码请求超时，将爬取下一篇文章。')
                            continue

                        temp_html.encoding = 'utf-8'
                        data = temp_html.text

                        # 加入反防盗链标签
                        html = re.sub(pattern='<head>', repl='<head><meta name="referrer" content="never">', string=data)
                        # 显示二维码
                        html = re.sub(pattern='id="js_pc_qr_code_img"', repl='id="pc_qr_code_img" src="%s"' % qr_code_path, string=html)
                        # 显示二维码
                        html = re.sub(pattern='id="js_profile_qrcode_img"', repl='id="profile_qrcode_img" src="%s"' % qr_code_path, string=html)



                        # 文章文字数量
                        temp_content = content.replace("\n", "")
                        temp_content = temp_content.strip()
                        word_amount = len(temp_content)

                        # 文章图片数量
                        img_amount = 0

                        # 文字视频数量
                        video_amount = 0

                        # 文章音频数量
                        audio_amount = len(re.findall('audio_iframe', html, re.S))

                        # 依次将data-src替换为本地路径
                        path_name = '../../static/wechat_imgs/'  # 存储图片的路径
                        for img_name in imgs:
                            if img_name == 'video':
                                video_amount += 1
                                html = re.sub(pattern='data-src', repl='src', string=html, count=1)
                            else:
                                img_amount += 1
                                img = path_name+img_name
                                html = re.sub(pattern='data-src=".*?"', repl='src="%s"' %img, string=html, count=1)


                        # html写入项目当前目录的HTML文件夹，文件名为标题前10个字，需要使用可删除注释
                        # f = open('HTML/'+title[:10]+'.html', 'a+')
                        # f.write(html)
                        # f.close()

                        # 保存数据到数据库
                        sql = 'INSERT INTO wechat_article(publish_date,article_title,wechat_id,article_url,cover_img,article_content,article_html,img_amount,word_amount,video_amount,audio_amount) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
                        # 推文为分享其他文章则不入库
                        if content != 'null':
                            try:
                                self.cursor.execute(sql,(pdate, title, wechat_id, article_url, path_cover+cover_name, content, html, img_amount, word_amount, video_amount, audio_amount))
                                self.db.commit()
                                Log.article_log(u'入库成功')
                            except:
                                self.db.rollback()
                                Log.article_log(u'入库不成功')
                        else:
                            Log.article_log(u'文章内容为null')

        self.db.close()
        print('\n')
        Log.article_log('爬虫已完成任务 ')

    def get_atticle_info(self,url):
        '''
        获取文章详细内容
        :param url:
        :return:
        '''
        try:
            html = requests.get(url,headers=self.headers, timeout=self.timeout)
        except:
            return 'timeout'

        soup = BeautifulSoup(html.text,"lxml")
        content = soup.find('div', id='img-content')

        temp_contents = re.findall('此(.*?)无法查看', html.text, re.S)

        if len(temp_contents) > 0:
            if '内容因违规' in temp_contents[0]:
                return 'null'

        p_list = []

        try:
            ps = content.find_all('p')
            for i in ps:
                x = i.get_text()
                p_list.append(x)

            main_content = '\n'.join(p_list)
        except:
            return "null"                   #异常则返回null

        return main_content

    def get_article_img(self,url):
        '''
        获取文章图片
        :param url:
        :return:
        '''

        try:
            res = requests.get(url, headers=self.headers, timeout=self.timeout)
        except:
            return 'timeout'

        if res.status_code == 200:
            contents = re.findall('data-src="(.*?)"', res.text, re.S)

        imgs = []
        path = '../../static/wechat_imgs/'

        for img in contents:
            # 随机生成一个长度为30的字符串，作为图片的文件名
            ran_str = (''.join(random.sample(string.ascii_letters + string.digits, 30)))
            if img.endswith('jpg'):
                img_name = ran_str + '.jpg'
                imgs.append(img_name)

                try:
                    data = requests.get(img, headers=self.headers, timeout=self.img_timeout)
                except:
                    return 'timeout'
                fp = open(path + img_name, 'wb')            # 下载图片到本地
                fp.write(data.content)
                fp.close()
            elif img.endswith('jpeg'):
                img_name = ran_str + '.jpeg'
                imgs.append(img_name)

                try:
                    data = requests.get(img, headers=self.headers, timeout=self.img_timeout)
                except:
                    return 'timeout'
                fp = open(path + img_name, 'wb')
                fp.write(data.content)
                fp.close()

            elif img.endswith('png'):
                img_name = ran_str + '.png'
                imgs.append(img_name)

                try:
                    data = requests.get(img, headers=self.headers, timeout=self.img_timeout)
                except:
                    return 'timeout'
                fp = open(path + img_name, 'wb')
                fp.write(data.content)
                fp.close()

            elif img.endswith('gif'):
                img_name = ran_str + '.gif'
                imgs.append(img_name)

                try:
                    data = requests.get(img, headers=self.headers, timeout=self.img_timeout)
                except:
                    return 'timeout'
                fp = open(path + img_name, 'wb')
                fp.write(data.content)
                fp.close()
            else:
                if img.startswith('https://mmbiz.qpic.cn/mmbiz_jpg'):
                    img_name = ran_str + '.jpg'
                    imgs.append(img_name)

                    try:
                        data = requests.get(img, headers=self.headers, timeout=self.img_timeout)
                    except:
                        return 'timeout'
                    fp = open(path + img_name, 'wb')  # 下载图片到本地
                    fp.write(data.content)
                    fp.close()

                elif img.startswith('https://mmbiz.qpic.cn/mmbiz_jpeg'):
                    img_name = ran_str + '.jpeg'
                    imgs.append(img_name)

                    try:
                        data = requests.get(img, headers=self.headers, timeout=self.img_timeout)
                    except:
                        return 'timeout'
                    fp = open(path + img_name, 'wb')
                    fp.write(data.content)
                    fp.close()

                elif img.startswith('https://mmbiz.qpic.cn/mmbiz_png'):
                    img_name = ran_str + '.png'
                    imgs.append(img_name)

                    try:
                        data = requests.get(img, headers=self.headers, timeout=self.img_timeout)
                    except:
                        return 'timeout'
                    fp = open(path + img_name, 'wb')
                    fp.write(data.content)
                    fp.close()

                elif img.startswith('https://mmbiz.qpic.cn/mmbiz_gif'):
                    img_name = ran_str + '.gif'
                    imgs.append(img_name)

                    try:
                        data = requests.get(img, headers=self.headers, timeout=self.img_timeout)
                    except:
                        return 'timeout'
                    fp = open(path + img_name, 'wb')
                    fp.write(data.content)
                    fp.close()

                elif img.startswith('https://v.qq.com/iframe'):
                    img_name = 'video'
                    imgs.append(img_name)

        return imgs

class AccountSpider:
    '''
    公众号信息爬虫，用户爬取公众号名称、头像等
    '''
    def __init__(self, wechat_ids):
        '''
        构造函数，根据公众号微信号获取对应公众号名称、头像等信息
        :param
        '''
        self.wechat_ids = wechat_ids

        # 请求头
        self.headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

        # 超时时长
        self.timeout = 5

        # 图片爬取超时时长
        self.img_timeout = 10

        # 爬虫模拟在一个request.session中完成
        self.session = requests.Session()

        # 连接数据库
        # self.db = sqlite3.connect('../../bee-database.db')
        self.db = sqlite3.connect('bee-database.db')
        self.cursor = self.db.cursor()


    def get_account_infos(self):
        wechat_accounts_list = []
        print(self.wechat_ids)

        Log.account_log('正在爬取公众号信息。。。')
        for wechat_id in self.wechat_ids:

            time.sleep(1)
            print('\n')
            Log.account_log(u'公众号id为：%s' % wechat_id)

            # 先进行查询数据库是否存在此条记录
            sql1 = "SELECT wechat_id, wechat_name FROM wechat_account WHERE wechat_id='" + wechat_id + "'"
            self.cursor.execute(sql1)
            exits = self.cursor.fetchall()  # 查找所有符合条件的数据
            if len(exits) >= 1:
                Log.account_log(u'公众号名称：%s' % exits[0][1])
                Log.account_log('数据已存在，忽略此次爬取.')
                continue

            # 搜索url
            search_url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query=' + wechat_id

            try:
                search_html = self.session.get(search_url,headers=self.headers, timeout=self.timeout).content
            except:
                Log.account_log('请求超时，将爬取下一个公众号。')
                continue

            # 获取公众号URL
            doc = pq(search_html)
            wechat_url = doc('div[class=txt-box]')('p[class=tit]')('a').attr('href')

            # 获取html
            browser = webdriver.Chrome()
            browser.get(wechat_url)
            time.sleep(2)
            wechat_html = browser.execute_script("return document.documentElement.outerHTML")
            browser.close()

            # 检测是否被限制访问
            if pq(wechat_html)('#verify_change').text() != '':
                Log.account_log(u'已限制访问，请稍后再试')

            else:
                doc = pq(wechat_html)
                account = doc('div[class="profile_info_group"]')

                # 获取公众号名称
                wechat_name = account('strong[class="profile_nickname"]').text().strip()
                Log.account_log(u'公众号名称：%s' % wechat_name)
                Log.account_log(u'公众号url：%s' % wechat_url)

                # 获取公众号头像
                head_portrait_url = account('img').attr('src')
                Log.account_log(u'头像url：%s' % head_portrait_url)

                # 获取公众号二维码图片
                temp_url = doc('#js_pc_qr_code_img').attr('src')
                qr_code_url = 'http://mp.weixin.qq.com' + temp_url
                Log.account_log(u'二维码url：%s' % qr_code_url)

                # path_head_portrait = '../../static/head_portraits/'
                path_head_portrait = 'static/head_portraits/'
                # path_qr_code = '../../static/qr_codes/'
                path_qr_code = 'static/qr_codes/'

                ran_str = (''.join(random.sample(string.ascii_letters + string.digits, 30)))
                head_portrait_name = ran_str + '.png'
                ran_str = (''.join(random.sample(string.ascii_letters + string.digits, 30)))
                qr_code_name = ran_str + '.jpeg'

                try:
                    head_portrait_data = requests.get(head_portrait_url, headers=self.headers, timeout=self.img_timeout)
                    qr_code_data = requests.get(qr_code_url, headers=self.headers, timeout=self.img_timeout)
                except:
                    Log.account_log('爬取图片超时，将爬取下一个公众号。')
                    continue

                # 保存数据到数据库
                sql = 'INSERT INTO wechat_account(wechat_id, wechat_name, head_portrait, qr_code) values(?, ?, ?, ?)'

                try:
                    self.cursor.execute(sql, (wechat_id, wechat_name, '/'+path_head_portrait+head_portrait_name, '/'+path_qr_code+qr_code_name))
                    self.db.commit()
                    Log.account_log(u'入库成功')
                    wechat_accounts_list.append({'wechat_id': wechat_id, 'wechat_name': wechat_name})

                    # 只有入库成功才下载到本地
                    fp = open(path_head_portrait + head_portrait_name, 'wb')
                    fp.write(head_portrait_data.content)
                    fp.close()

                    fp = open(path_qr_code + qr_code_name, 'wb')
                    fp.write(qr_code_data.content)
                    fp.close()

                except:
                    self.db.rollback()
                    Log.account_log(u'入库不成功')

        print('\n')
        Log.account_log('爬虫已完成任务 ')
        return wechat_accounts_list

if __name__ == '__main__':

    ids = ['chaping321', 'dglgtw', 'one', 'two', 'four', 'five']
    # wechat_ids = ['dglgtw', 'guanqingluntan', 'dutsmc', 'TNTstreetdance', 'DGUT_GGCY', 'dgutxn', 'ggxshwlb', 'ggrpfamily', 'dgutkob', 'dgutzb', 'dgutpx', 'guangongkexie', 'dgutgreen', 'yinzytravel', 'DGUTTKD', 'wailianjiating', 'ggsfxh', 'gh_93ff0d749e07', 'dgutnic', 'ggdxskjcxxx', 'ggdzzyz', 'dgutsyxh', 'dgutsy']
    wechat_ids = ['dglgtw', 'dglgxyxsh','dgut']

    AccountSpider(wechat_ids).get_account_infos()
    ArticleSpider(wechat_ids).get_infos()
