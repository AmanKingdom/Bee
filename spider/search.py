#encoding=utf-8

import time
import jieba
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
        self.db = pymysql.connect(host='localhost', user='root', password='dgut520!', port=3306, db='bee_database')
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
        words = self.cut_word(self.words)   # 调用分词函数
        infos = []                          # 外层列表，存储检索到的每条推文信息的子列表
        for word in words:
            sql = "SELECT id, article_title FROM wechat_article WHERE article_title LIKE '%" + word + "%'"
            self.cursor.execute(sql)
            datas = self.cursor.fetchall()  # 查找所有符合条件的数据

            if len(datas) > 0:

                for data in datas:
                    temp_word = '<font color="red">' + word + '</font>'  # 添加html标签
                    new_data = []                                       # 每条推文信息的子列表
                    new_data.append(data[0])                            # 主键id
                    new_data.append(data[1].replace(word, temp_word))   # 标题
                    infos.append(new_data)                              # 添加数据到外层列表

        for info in infos:
            self.log("查询到数据：%s" % info)
        self.db.close()
        return infos

if __name__ == '__main__':

    words = 'goole杀了500个2019年GitHub微软苹果科技脚本爬虫程序员祭天！'
    Search(words).search_infos()