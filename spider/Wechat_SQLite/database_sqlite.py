
import time
import sqlite3


def log(msg):
    '''
    日志函数
    :param msg: 日志信息
    :return:
    '''
    print(u'%s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg))

def create_databases():
    '''
    创建数据库
    :return:
    '''
    db = sqlite3.connect('bee-database.db')
    db.close()
    log('bee_database数据库已创建好')

def create_tables():
    '''
    创建表
    :return:
    '''

    db = sqlite3.connect('bee-database.db')
    cursor = db.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS wechat_article(id integer PRIMARY KEY autoincrement,publish_date VARCHAR(20) NOT NULL,article_title VARCHAR(200) NOT NULL,wechat_id VARCHAR(20) NOT NULL,article_url TEXT NOT NULL,cover_img TEXT NOT NULL,article_content TEXT,article_img TEXT,article_html MEDIUMTEXT)'
    cursor.execute(sql)
    db.close()
    log('wechat_article表已创建好')

def create_index():
    '''
    创建唯一索引
    :return:
    '''
    db = sqlite3.connect('bee-database.db')
    cursor = db.cursor()
    sql = 'CREATE UNIQUE INDEX unique_index ON wechat_article (publish_date,article_title)'
    cursor.execute(sql)
    db.close()
    log('unique_index索引已创建好')

def delete_database():
    '''
    删除数据库
    :return:
    '''
    db = sqlite3.connect('bee-database.db')
    cursor = db.cursor()
    sql = 'DROP DATABASE bee_database'
    confirm = input('确定删除bee_database数据库？Y/N:')
    while 1:
        if confirm == 'Y':
            cursor.execute(sql)
            log('bee_database数据库已删除')
            return
        elif confirm == 'N':
            log('取消删除bee_database数据库')
            return
        else:
            log('输入有误！')
            confirm = input('确定删除bee_database数据库？Y/N:')
    db.close()

def delete_table():
    '''
    删除表
    :return:
    '''
    db = sqlite3.connect('bee-database.db')
    cursor = db.cursor()
    sql = 'DROP TABLE wechat_article'
    confirm = input('确定删除wechat_article表？Y/N:')
    while 1:
        if confirm == 'Y':
            cursor.execute(sql)
            log('wechat_article表已删除')
            return
        elif confirm == 'N':
            log('取消删除wechat_article表')
            return
        else:
            log('输入有误！')
            confirm = input('确定删除wechat_article表？Y/N:')
    db.close()

def insert():
    sql = 'INSERT INTO wechat_article(publish_date,article_title,wechat_id,article_url,cover_img,article_content,article_img,article_html) values(?, ?, ?, ?, ?, ?, ?, ?)'
    date1 = '20182'
    title = 'title1'
    wechat_id = 'id'
    article_url = 'url'
    pic = 'oic'
    content = 'content'
    imgs = 'img'
    html = 'html'
    db = sqlite3.connect('bee-database.db')
    cursor = db.cursor()
    cursor.execute('INSERT INTO wechat_article(publish_date,article_title,wechat_id,article_url,cover_img,article_content,article_img,article_html) values(?,?,?,?,?,?,?,?)',(date1, title, wechat_id, article_url, pic, content, imgs, html))
    db.commit()
    log(u'入库成功')


if __name__ == '__main__':
    while 1:
        print('\n1-创建数据库  |  2-创建数据表')
        print('3-建立唯一索引  |  4-删除数据表  |  0-退出')
        choose = input('请选择：')
        if choose == '1':
            create_databases()

        elif choose == "2":
            create_tables()

        elif choose == "3":
            create_index()

        elif choose == "4":
            delete_table()

        elif choose == '0':
            break

        else:
            print("选择有误")