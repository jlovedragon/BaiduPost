#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'quantin'

'''
百度贴吧爬虫：
1. 先以中国科学技术大学吧为例，熟悉百度贴吧发帖规则与流程
2. 数据实体：
    2.1 postHttp    帖子唯一链接(string)
    2.2 postTitle   帖子标题(string)
    2.3 authorName  作者姓名(string)
    2.4 authorID    作者ID(string)
    2.5 postNo      帖子所在楼层(int)
    2.6 postType    帖子类型(string, 1开贴文、2跟帖文、3回复)
    2.7 replyTo     回复给谁(string, 只能拿到name,无法拿到ID)
    2.8 postContent 帖子内容
    2.9 postTime    帖子发表时间

'''

import requests
from bs4 import BeautifulSoup

import time
import json

postFile = open('/Users/quantin/data/baidu/baiduPost.txt', 'a+')

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
            jTopicName = jTopicAtt.text
            # print jTopicName
            jReplyTime = jTopic.find_all('span', 'threadlist_reply_date j_reply_data')[0].text
            jHref = jTopicAtt['href']
            getTextEveryTopic(jTopicName, jHref)


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

def getTextEveryTopic(jTopicName, jHref):
    topicUrl = 'http://tieba.baidu.com' + jHref
    print jTopicName + '\t' + topicUrl
    try:
        topicResp = requests.get(topicUrl)
        topicResp.encoding = 'utf-8'
        topicSoup = BeautifulSoup(topicResp.text, 'lxml')

        # author = topicSoup.find_all('a', 'p_author_name')[0].text
        # print author

        topicPageNum = int(topicSoup.find_all('li', 'l_reply_num')[0].find_all('span', 'red')[1].text)
        for kPage in range(1, topicPageNum + 1):
            items = topicSoup.find_all('div', 'l_post')
            for item in items:
                dataField = item['data-field']
                jsonData = json.loads(dataField, encoding='utf-8')
                authorName = jsonData['author']['user_name']
                authorID = jsonData['author']['user_id']
                postNo = jsonData['content']['post_no']
                postContent = item.find_all('div', 'p_content')[0].text.strip()

                postTime = item.find_all('span', 'j_reply_data')[0].text
                print postContent + '\t' + postTime


    except:
        print "None"



if __name__ == '__main__':
    main()