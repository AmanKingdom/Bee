# coding=gbk
from gensim import corpora, models, similarities
import jieba
import time
import sqlite3

class SimilarityJudge:
    '''
    �������ƶ��ж�
    '''

    def __init__(self):
        '''

        :param key_text: �û���д������
        :param compared_text: ���ݿ�������ϵ�����
        '''

        # self.key_text = key_text
        # self.compared_text = compared_text

    def log(self, msg):
        '''
        ��־����
        :param msg: ��־��Ϣ
        :return:
        '''
        print(u'%s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg))

    def cut(self, text):
        '''
        �ִʺ���
        :return:
        '''
        generator = jieba.cut(text)
        return [word for word in generator]


    def judgement(self,key_text,compared_text):
        '''
        ���ƶ��жϺ���
        :return: ���ƶ�
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

        # ���ƶȼ���
        index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=feature_cnt)
        # print('\nTF-IDFģ�͵�ϡ����������')
        # for i in tfidf[corpus]:
        #     print(i)
        # print('\nTF-IDFģ�͵�keywordϡ��������')
        # print(tfidf[new_vec])

        sim = index[tfidf[new_vec]]
        # self.log("���ƶȣ�%s" % sim[0])
        return sim[0]


    def get_info(self):
        '''
        ��ȡ���ݿ������
        :return: datas
        '''

        db = sqlite3.connect('bee-database.db')
        cursor = db.cursor()

        sql = "SELECT id, article_title, article_content FROM wechat_article "
        sql1 = "SELECT id, article_title, article_content FROM app_blogarticle"
        cursor.execute(sql)
        wechat_datas = cursor.fetchall()  # �������з�������������
        cursor.execute(sql1)
        blog_datas = cursor.fetchall()  # �������з�������������
        db.close()

        datas = wechat_datas + blog_datas

        return datas

    def operation(self, key, value):
        '''
        �ж����ƶȲ�������
        :return:���ƶ� >= value ʱ���ظ����ƶȣ����򷵻�0
        '''
        datas = self.get_info()
        value_datas = []

        for data in datas:
            compared_text = data[2]
            compared_text = compared_text.replace("\n", "")
            # print(com)

            # print(data[1])
            temp_value = SimilarityJudge().judgement(key,compared_text)
            self.log("���ƶȣ�%s" % temp_value)
            value_datas.append(temp_value)
            # if temp_value >= value:
            #     return temp_value
        return max(value_datas)

if __name__ == '__main__':


    # �û���д������
    key_text = '''����3-4�յĻ�����ոս���?�������ǵľ�Ӣ���������ˣ�@У����֯��������ѧ��֯�����������������ϯ�����������������Ǻܺ��������Լ����������������Ǵ�����⡰���ѧ�����ס��ֺܾ��ᣬû��ѹ�����Ը����Ǿ�����������Ǻ����Ľ��뿼���ڸ����Ǳ���ѹ�����������ÿ������ۣ��ʾ���֭���ǲ�����Ҳ��ּ尾�᲻�ø��µ��е�ÿһ�������������ѡ������ӭ������һ��С�������ڿ��ĵ�ͬʱҲ��ʼæµ������ʼ���ֲ��Ź�������Ϊ ���������ɶ��˵��Ǹ������������ƵƵ���ָ���֮������϶���Ҫ������������ȥ��ȴҲ������ͷ����β���������Լ�Ū�������Ǻܰ������Լ�Ҫ����߻����Լ��������廹��С���¸����������ڲ�����ܺ�������������˵��û�ա�����û���뵽���������Ϣ���˺ü���Сʱʼ��û��һ���˻ظ���������ܲ�����ȥ˽�ĸ����ǻ��Ե���ʩ��ѹ��������⡰��Ҷ�æ���ɣ�����ʼ�ջ������������ŵ�δ�����ÿ���һ����������������Ὺ����ͣ�Ӳ���Ĺ���΢�ź�����ʱ�򣬲������Լ�������Ҳ�����Լ����뷨��������Դ�ҵ����������о����ǿ�Ҫ������Ҳ�����ǻ������ָо�����ֻ�ǵ�һ������������Ϊʲô����ô�ۣ��������������������������ܵ��ģ����������Լ�������Ҫ���������Ƿ����������ôһ���ط�����һȺӵ����ͬ���룬��ͬ�������һ�����������ڽ����Ĺ�����һ��ѧϰ��ν����Щ����Ȼ����˼��ѧϰ�н�������������������ﲻһ������������¿�ʼ������������ҵ��������Լ���������������ο�ʼ�ĵط�������ǵ�ʮ���ھ�Ӣ�࣡�����������ʶ������һ���������ǻ�һ������������ĸ���ѧϰ��ʮ�˴���������ָ����������������ֵķ�Χ�еõ����ʵ���չ��ʶһ�����꣬����һ������ѧ��ȥ�����Լ���������״̬�����ʵ�����������ⶼ�����õ����㶨λ�Լ�����ʵ�Լ����Լ��õ������Ķ�����Ϊ�����ľ�Ӣ����Ӣ�࿪��֮ǰС��ϣ����ҿ��Դ�����ǻ��Ѫ�Լ�С���ǵ���������ѧϰ��������������ջ�һ��Ŭ����ɣ������������������λС�ɰ��Բ����ı�װɣ�����д��̫���ˣ���Ҫ���������ٶ�ҲҪд����Ҫ����Լ���������д��д����ʹ����д��д�������Ĳ����ǲŻ��Ѽ��������º�ȫ���ǰ���������������ۣ���Ӣ������������Ҫһ����գ���Ҫ���������ǵľ�Ӣ����صġ����ּ�������Ƭ����ʽ��Զ���������ֻ�������Լ�����׼��������������һ���ڴ���Ӣʮ�����������Σ�һ���ź���Ӣʮ��������������Ѽ��@������&С������û������д�������ϣ�������λ�ò�����д���Ǿ�д������ɣ���ʲô��Ҫ���Լ���С������&������˵��һ�������۴�д�¸������ǰɣ�

'''
    key_text = key_text.replace("\n", "")


    # �������ƶȷ�ֵ
    value =0.9

    # ���ƶȴ���value�ͷ��ظ�ֵ�����򷵻� 0
    aa = SimilarityJudge().operation(key_text,value)
    print(aa)




