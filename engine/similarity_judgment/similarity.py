# coding=gbk
from gensim import corpora, models, similarities
import jieba
import time
import sqlite3

class SimilarityJudge:
    '''
    文章相似度判断
    '''

    def __init__(self):
        '''

        :param key_text: 用户编写的文章
        :param compared_text: 数据库或网络上的文章
        '''

        # self.key_text = key_text
        # self.compared_text = compared_text

    def log(self, msg):
        '''
        日志函数
        :param msg: 日志信息
        :return:
        '''
        print(u'%s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg))

    def cut(self, text):
        '''
        分词函数
        :return:
        '''
        generator = jieba.cut(text)
        return [word for word in generator]


    def judgement(self,key_text,compared_text):
        '''
        相似度判断函数
        :return: 相似度
        '''

        texts = [compared_text, '']
        key_text = key_text

        texts = [self.cut(text) for text in texts]
        # print(texts)

        dictionary = corpora.Dictionary(texts)
        feature_cnt = len(dictionary.token2id.keys())
        corpus = [dictionary.doc2bow(text) for text in texts]
        tfidf = models.TfidfModel(corpus)
        new_vec = dictionary.doc2bow(self.cut(key_text))

        # 相似度计算
        index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=feature_cnt)
        # print('\nTF-IDF模型的稀疏向量集：')
        # for i in tfidf[corpus]:
        #     print(i)
        # print('\nTF-IDF模型的keyword稀疏向量：')
        # print(tfidf[new_vec])

        sim = index[tfidf[new_vec]]
        # self.log("相似度：%s" % sim[0])
        return sim[0]


    def get_info(self):
        '''
        获取数据库的数据
        :return: datas
        '''

        db = sqlite3.connect('bee-database.db')
        cursor = db.cursor()

        sql = "SELECT id, article_title, article_content FROM wechat_article "
        sql1 = "SELECT id, article_title, article_content FROM app_blogarticle"
        cursor.execute(sql)
        wechat_datas = cursor.fetchall()  # 查找所有符合条件的数据
        cursor.execute(sql1)
        blog_datas = cursor.fetchall()  # 查找所有符合条件的数据
        db.close()

        datas = wechat_datas + blog_datas

        return datas

    def operation(self, key, value):
        '''
        判断相似度操作函数
        :return:相似度 >= value 时返回该相似度，否则返回0
        '''
        datas = self.get_info()
        value_datas = []

        for data in datas:
            compared_text = data[2]
            compared_text = compared_text.replace("\n", "")
            # print(com)

            # print(data[1])
            temp_value = SimilarityJudge().judgement(key,compared_text)
            self.log("相似度：%s" % temp_value)
            value_datas.append(temp_value)
            # if temp_value >= value:
            #     return temp_value
        return max(value_datas)

if __name__ == '__main__':


    # 用户编写的文章
    key_text = '''本月3-4日的基础班刚刚结束?属于你们的精英班马上来了！@校级组织副部长团学组织正部长副书记助理主席助理们面试招新你们很害怕由于自己过于严厉给干事们带来误解“这个学长好凶”又很纠结，没有压力面试干事们觉得这个部门是很随便的进入考核期干事们倍感压力，尽力完成每项工作很累，绞尽脑汁可是部长们也万分煎熬舍不得干事当中的每一个但必须得做出选择终于迎来了新一届小干事们在开心的同时也开始忙碌起来开始接手部门工作本以为 这下子轻松多了但是各项工作交接问题频频出现干事之间的契合度需要提高任务分配下去了却也往往从头跟到尾，甚至比自己弄还累你们很懊恼是自己要求过高还是自己表述不清还是小干事根本不想做内部建设很害怕听到干事们说“没空”但，没有想到的是这个消息发了好几个小时始终没有一个人回复你们心里很不好受去私聊干事们会显得在施加压力你们理解“大家都忙”可，工作始终还得有人做部门的未来还得靠大家还有这样那样的例会开个不停加不完的工作微信好友有时候，不仅是自己干事们也会有自己的想法、情绪面对大家的消极情绪感觉你们快要崩溃了也许你们会有这种感觉”我只是第一次做部长啊！为什么会这么累！“或许你会有许多许多的困扰你会很担心，甚至怀疑自己甚至想要放弃！你是否曾想过有这么一个地方你会和一群拥有相同梦想，相同困惑的人一起在这倾诉在交流的过程中一起学习如何解决这些问题然后在思考学习中进步！你可以相信在这里不一样的生活会重新开始在这里你可以找到真正的自己在这里或许是你梦开始的地方！这里，是第十二期精英班！在这里你会认识许多和你一样的人你们会一起接受心理讲座的辅导学习团十八大精神对生活的指导意义会在轻松娱乐的氛围中得到素质的拓展结识一份友谊，领悟一份真理学会去调整自己的情绪和状态解决现实遇到的困扰这都将更好地让你定位自己，充实自己让自己得到真正的锻炼成为真正的精英！精英班开班之前小编希望大家可以带着满腔热血以及小干们的期望用心学习、体验从中有所收获一起努力冲吧！最后让我们来看看各位小可爱对部长的表白吧！他们写得太多了，我要往上爬！再多也要写，我要表达自己的心声！写啊写啊！使劲儿写！写得满满的部长们才会冲鸭！给你起绰号全都是爱你的语气，加油哇！精英班来啦！我们要一起合照！我要把属于我们的精英班相关的、快乐记忆以照片的形式永远珍藏起来，只给我们自己看！准备好了吗？让我们一起期待精英十二，立德筑梦！一起呐喊精英十二我们来啦！冲鸭！@部长们&小干事们没有亲自写到海报上？或者是位置不够你写？那就写在这里吧！有什么想要和自己的小干事们&部长们说的一起在评论处写下告诉他们吧！

'''
    key_text = key_text.replace("\n", "")


    # 设置相似度筏值
    value =0.9

    # 相似度大于value就返回该值，否则返回 0
    aa = SimilarityJudge().operation(key_text,value)
    print(aa)




