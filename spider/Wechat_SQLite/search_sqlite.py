#encoding=utf-8

import time
import jieba
import sqlite3
import pymysql

class Search:
    def __init__(self,words):
        '''
        构造函数
        :param words:
        '''

        # 获取关键词
        self.words = words

        # 连接数据库
        self.db = sqlite3.connect('../../bee-database.db')
        self.cursor = self.db.cursor()

    def log(self,msg):
        '''
        日志函数
        :param msg: 日志信息
        :return:
        '''
        print(u'%s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg))

    def cut_word(self,words):
        '''
        利用jieba库的搜索引擎模式分词
        :param word:
        :return: 分词列表
        '''

        # 搜索引擎模式分词
        seg_list = list(jieba.cut_for_search(words))
        new_list = []

        # 提取大于等于两个字的词语
        for lists in seg_list:
            if len(lists) >= 2:
                new_list.append(lists)

        return new_list

    def search_infos(self):
        '''
        根据分词查询数据
        :param words:
        :return: 数据列表
        '''
        temp_words = self.cut_word(self.words)                          # 调用分词函数
        words = sorted(temp_words, key=lambda i: len(i), reverse=True)  # 按分词元素长度降序排序
        # print(words)

        infos = []                          # 外层列表，存储检索到的每条推文信息的子列表
        ids = []                            # 记录已匹配的文章id
        for word in words:
            sql = "SELECT id, article_title, article_content, publish_date, wechat_id FROM wechat_article WHERE article_title LIKE '%" + word + "%' OR article_content LIKE '%" + word + "%'"
            self.cursor.execute(sql)
            datas = self.cursor.fetchall()  # 查找所有符合条件的数据

            if len(datas) > 0:

                for data in datas:

                    if data[0] in ids:      # 不重复匹配同一篇文章
                        continue

                    linelist = [line.strip() for line in data[2].split('\n') if len(line) > 3]  # 将全文按行\n存入列表
                    temp_word = '<font color="red">' + word + '</font>'                         # 添加html标签

                    content = []
                    title = data[1].replace(word, temp_word)

                    if word in data[2]:

                        index = 0                   # 记录已匹配行数
                        word_num = 0                # 记录已匹配字数
                        for line in linelist:       # 分行检索

                            if word in line:

                                if index < 2:       # 匹配行数够两行后不再匹配
                                    index += 1
                                    content.append(line.replace(word, temp_word))
                                    word_num += len(line)

                            if word_num >= 100:     # 字数够100字后退出此关键字的匹配
                                break
                            else:
                                if index > 1 and index < 2:         # 匹配行数够两行而字数不够100就添加其他行作为内容
                                    index += 1
                                    content.append(line)

                    else:
                        content = linelist[3]+','+linelist[4]    # 文章内容无关键字暂且提取第4/第5行

                    new_data = {
                        'article_id' : data[0],
                        'publish_date': data[3],
                        'wechat_id': data[4],
                        'article_title' : title,
                        'article_content' : content
                    }
                    ids.append(data[0])             # 记录已经匹配过的文章
                    infos.append(new_data)          # 添加字典数据到列表

        for info in infos:
           self.log("查询到数据：%s" % info)
        self.db.close()
        return infos

if __name__ == '__main__':

    words = '占座'

    Search(words).search_infos()