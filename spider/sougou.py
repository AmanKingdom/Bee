# coding=utf-8

from selenium import webdriver
import time
import requests
from lxml import etree
driver_sougou = webdriver.Chrome()
#driver_change = webdriver.Chrome()

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}

#driver_sougou.get("http://weixin.sogou.com/")
#driver_sougou.find_element_by_xpath('//*[@id="loginBtn"]').click()     #模拟点击登录按钮
base_url = 'https://mp.weixin.qq.com'

f = open('/Users/one/PycharmProjects/WeChat/html.txt ','a+')

def get_url_list():
    '''
    获取公众号推文url列表
    :return:
    '''
    #account1 = input("请输入公众号名称：")
    account = "差评"
    #driver_sougou.find_element_by_xpath('//*[@id="query"]').send_keys("%s" % account)       #输入公众号
    #driver_sougou.find_element_by_xpath('//*[@id="searchForm"]/div/input[4]').click()       #模拟点击搜索公众号

    driver_sougou.get("https://weixin.sogou.com/weixin?type=1&query="+account)
    time.sleep(1)
    link = driver_sougou.find_element_by_xpath('//*[@class="news-box"]/ul/li[1]/div/div[2]/p/a')      #获取公众号详情页面
    init_url = link.get_attribute('href')
    driver_sougou.get(init_url)     #get公众号详情页面

    #print(driver_sougou.current_url)
    #print(driver_sougou.page_source)
    items = driver_sougou.find_elements_by_xpath('//*[@class="weui_media_bd"]/h4')      #获取所有推文的链接
    url_list = []
    for item in items:
        temp_url = item.get_attribute("hrefs")
        url_list.append(base_url + temp_url)

    print(url_list)

    html = requests.get(url_list[1])
    html.encoding = 'utf-8'
    f.write(html.text)
    f.close()

    time.sleep(3)
    #driver_sougou.close()


def get_info(url):
    '''
    获取推文信息
    :param url:
    :return:
    '''
    html = requests.get(url,headers=headers)
    selector = etree.HTML(html.text)



if __name__ == '__main__':
    get_url_list()
