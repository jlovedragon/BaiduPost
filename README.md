# BaiduPost

### 百度贴吧爬虫

##### 思路

1. 先以中国科学技术大学为例，熟悉百度贴吧发帖回复等规则

2. 帖子的排序是以最后的动态为准，而帖子内部回复则会放在尾页，故再爬取帖子列表时从第一页开始，在抓取帖子内部的动态时从尾页开始
3. 抓取频率初步设定为两个小时

##### 数据实体
| 属性 | 说明 | 类型 |
| --- | :---| ---|
| postHttp | 帖子唯一链接 | string |
| postTitle | 帖子标题 |string|
| authorID | 作者ID | string|
| authorName | 作者姓名 | string|
| postNo | 帖子所在楼层 | string|
| postType| 帖子类型，1开帖文、2跟帖文、3回复|string|
| replyTo |回复给谁|string|
| postContent |帖子内容|string|
| postTime | 帖子发表时间 | string |

如果是开帖文，replyTo为Null
跟帖文，replyTo为Null
所在楼层的回复如果包含回复，则replyTo为回复的人，否则为该楼层作者

##### 作者信息
```
author = 'quantin'
email  = 'jlove.dragon@gmail.com'
```
