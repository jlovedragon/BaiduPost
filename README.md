# BaiduPost

### 百度贴吧爬虫

##### 思路

1. 先以中国科学技术大学为例，熟悉百度贴吧发帖回复等规则

2. 帖子的排序是以最后的动态为准，而帖子内部回复则会放在尾页，故再爬取帖子列表时从第一页开始，在抓取帖子内部的动态时从尾页开始
3. 抓取频率初步设定为两个小时

##### 数据实体
| 属性 | 说明 | 类型 |
| --- | :---| ---|
| author | 作者| string |
| timestamp| 时间戳，13位数字|string|
|type|文本类型，1开帖文、2跟帖文、3评论、4回复|string|
|belongTo|所属帖子ID，10位数字|string|
|replyTo|回复给谁|string|
|http| 该帖子对应的HTTP |string|
|content|帖子内容|string|
|contentSource|回复的源文本|string|


##### 作者信息
```
author = 'quantin'
email  = 'jlove.dragon@gmail.com'
```
