import requests
from lxml import etree
import pypinyin
import time
from xpinyin import Pinyin
headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
news = []
technlg = []
car = []
house = []
job = []
finance = []
life = []
inspire = []
female = []
travel = []
sport = []
cate = []
fun = []
star = []
infant = []
education = []
startup = []
governm = []
company = []
local = []


def get_account():
    types = [news, technlg, car, house, job, finance, life, inspire, female, travel, sport, cate, fun, star, infant,
             education, startup, governm, company, local]

    for category in range(1,21):
        url = 'https://data.wxb.com/rank?category='+str(category)+'&page=1'
        html = requests.get(url,headers=headers)
        selector = etree.HTML(html.text)
        type = selector.xpath('//div[@class="rank-right"]/div/text()')[0]
        p = Pinyin()
        print("==========")
        #print(p.get_pinyin(type))
        print("正在爬取类别：",type)
        print("==========")
        infos = selector.xpath('//tbody[@class="ant-table-tbody"]/tr')

        for info in infos:
            name = info.xpath('td[2]/div/div[2]/div[1]/a/text()')[0]
            #wechat_id = info.xpath('td[2]/div/div[2]/div[2]/text()')[0]
            types[category-1].append(name)
            #print(name)

        time.sleep(2)
    return types




if __name__ == '__main__':

    #print(get_account())

    lisys = get_account()

    for list in lisys:
        print(list)
        print("\n")

    print('ok')