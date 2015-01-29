#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'quantin'

'''
百度贴吧爬虫：
1. 先以中国科学技术大学吧为例，熟悉百度贴吧发帖规则与流程
2. 数据实体：
    2.1 postHttp    帖子唯一链接(string)
    2.2 postTitle   帖子标题(string)
    2.3 authorID    作者ID(string)
    2.4 authorName  作者姓名(string)
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
internal = 2
# 百度贴吧前缀
urlPrefix = 'http://tieba.baidu.com'


# 存入文件
def store(needWrite):
    postFile.write(needWrite)
    postFile.flush()

def getTextEveryTopic(jTopicName, jHref):
    topicUrl = 'http://tieba.baidu.com' + jHref
    print jTopicName + '\t' + topicUrl
    try:
        topicResp = requests.get(topicUrl)
        topicResp.encoding = 'utf-8'
        topicSoup = BeautifulSoup(topicResp.text, 'lxml')

        topicPageNum = int(topicSoup.find_all('li', 'l_reply_num')[0].find_all('span', 'red')[1].text)

        # 页码从后往前迭代，因为最新的帖子总是在最后面
        for kPage in range(topicPageNum, 0, -1):
            items = topicSoup.find_all('div', 'l_post')

            # 从后往前迭代，因为最新的帖子总是在最后面
            for m in range(len(items) - 1, -1, -1):
                postTime = items[m].find_all('span', 'j_reply_data')[0].text

                curTimeStamp = time.time()
                postTimeStamp = time.mktime(time.strptime(postTime,'%Y-%m-%d %H:%M'))

                # 抓取最近两个小时的帖子
                if int(curTimeStamp - postTimeStamp) < internal * 60 * 60:
                    dataField = items[m]['data-field']
                    jsonData = json.loads(dataField, encoding='utf-8')
                    authorName = jsonData['author']['user_name']
                    authorID = str(jsonData['author']['user_id']).decode('utf-8')
                    postNo = str(jsonData['content']['post_no']).decode('utf-8')
                    postType = '1' if postNo == '1' else '2'
                    postContent = items[m].find_all('div', 'p_content')[0].text.strip()

                    needWrite = (jHref + '\t' + jTopicName + '\t' + authorID + '\t' + authorName + '\t' + postNo + '\t' + postType.decode('utf-8') + '\t' + postContent + '\t' + postTime + '\n').encode('utf-8')

                    store(needWrite)
                else:
                    return "crawl finish"
                # postContentMain = item.find_all('div', 'd_post_content_main')[0]
                # print postContentMain + '------'

                # 是否帖子有回复
                # replyNum = int(jsonData['content']['comment_num'])
                # for replyItem in item.find_all('div', 'd_post_content_main')[0].find_all('li', 'lzl_single_post'):
                #     replyAuthor = replyItem.find_all('a', 'at j_user_card')[0].text
                #     replyContent = replyItem.find_all('span', 'lzl_content_main')[0].text
                #     print replyAuthor + '\t' + replyContent + '---------'
                #     # if replyContent.find('回复')
    except:
        print "None"

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

            # 如果最新回复不是今天的，则丢弃
            if jReplyTime.find('-') != -1:
                time.sleep(internal * 60)
            else:
                hour = int(jReplyTime.replace(' ', '')[0:2])
                # 只抓最近两个小时有更新的帖子
                currentHour = int(time.strftime("%H",time.localtime()))
                if hour >= currentHour - internal:
                    jHref = jTopicAtt['href']
                    getTextEveryTopic(jTopicName, jHref)

    postFile.close()

if __name__ == '__main__':
    main()