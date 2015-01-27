#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'quantin'

'''
百度贴吧爬虫：
1. 先以中国科学技术大学吧为例，熟悉百度贴吧发帖规则与流程
2. 
'''

import requests
from bs4 import BeautifulSoup

import time
import json

# 每隔多长时间抓一次
internal = 20
# 百度贴吧前缀
urlPrefix = 'http://tieba.baidu.com'

# 主函数
def main():
    url = "http://tieba.baidu.com/f?kw=%E4%B8%AD%E5%9B%BD%E7%A7%91%E5%AD%A6%E6%8A%80%E6%9C%AF%E5%A4%A7%E5%AD%A6&ie=utf-8"
    respond = requests.get(url)
    respond.encoding = 'utf-8'

    mainSoup = BeautifulSoup(respond.text, 'lxml')
    # 主题数
    topicNum = int(mainSoup.find_all('span', 'red')[0].text)
    pageNum = topicNum / 50
    for iPage in range(0, pageNum):
        print iPage
        pageUrl = url + '&pn=' + str(iPage * 50)
        iPageResp = requests.get(pageUrl)
        iPageResp.encoding = 'utf-8'
        iPageSoup = BeautifulSoup(iPageResp.text, 'lxml')
        topicList = iPageSoup.find_all("li", "j_thread_list clearfix")
        for jTopic in topicList:
            jTopicAtt = jTopic.find_all('a', 'j_th_tit')[0]
            # print jTopicName
            jReplyTime = jTopic.find_all('span', 'threadlist_reply_date j_reply_data')[0].text
            jHref = jTopicAtt['href']
            getTextEveryTopic(jHref)


            '''
            # 如果最新回复不是今天的，则丢弃
            if jReplyTime.find('-') != -1:
                return
            else:
                hour = int(jReplyTime.replace(' ', '')[0:2])
                # 只抓最近两个小时有更新的帖子
                currentHour = int(time.strftime("%H",time.localtime()))
                if hour >= currentHour - internal:
                    jHref = jTopicAtt['href']
                    getTextEveryTopic(jHref)
            '''

def getTextEveryTopic(jHref):
    topicUrl = 'http://tieba.baidu.com' + jHref
    try:
        topicResp = requests.get(topicUrl)
        topicResp.encoding = 'utf-8'
        topicSoup = BeautifulSoup(topicResp.text, 'lxml')

        author = topicSoup.find_all('a', 'p_author_name')[0].text
        print author
        topicPage = int(topicSoup.find_all('li', 'l_reply_num')[0].find_all('span', 'red')[1].text)
        if topicPage == 1:
            items = topicSoup.find_all('div', 'l_post')
            for item in items:
                data = item['data-field']
                print data
                jsonData = json.loads(data, encoding='utf-8', )
                print type(jsonData)
                print jsonData['author']['user_id']
        else:
            for kPage in range(2, topicPage + 1):
                pass
    except:
        print "None"



if __name__ == '__main__':
    main()