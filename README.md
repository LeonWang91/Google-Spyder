# Google-Spyder

## Google搜索引擎关键词检索结果抓取 ##

### 程序功能 ###

- [x] 支持配置文件设置
- [x] 支持分时间段爬取
- [x] 支持自定义关键词爬取
- [x] 支持随机切换Google域名
- [x] 支持爬取结果过程日志记录
- [x] 支持爬取结果写入CSV或数据库

### 数据字段 ###

- title：标题信息
- caption_cite：二级链接
- caption_time：发布时间
- caption_p：摘要信息

**数据字段以列表形式存储，长度应一致，某一字段不存在则为None。**

### 运行记录 ###

```
[~] Read configuration file

[+] Read complete

Page1：https://www.google.pn/search?hl=en&q=Confucius+Institute&tbs=cdr:1,cd_min%3A7/28/2022,cd_max:7/19/2022&start=0

title：9		caption_cite：9		caption_time：9		caption_p：9

......

 Page17：https://www.google.it/search?hl=en&q=Confucius+Institute&tbs=cdr:1,cd_min%3A7/28/2022,cd_max:7/19/2022&start=160

 title：158		caption_cite：158		caption_time：158		caption_p：158

-----------------------------------------------------------------------------------------------

------Stored in the database------

------End------
```

### 常见报错 ###

- 网页获取错误
- - 网页源代码无法获取，或者出现Connect链接问题报错
- 网页解析错误
- - 数据字段长度不一致，写入文件时报错

### 解决方案 ###

- 可能是谷歌网页大量爬取后需要人机验证，可以点击抓取失败的当前链接查看
- 更换代理：可以更换ip+端口（使用代理池），或者更换代理的节点（一般换节点就能解决）

### 程序演示 ###

![Program running log](https://user-images.githubusercontent.com/60532543/185627888-d3d4aed3-6aed-4f99-a542-a342b08b9299.gif)


### 关于博主 ###

#### 知乎：[南浔Pyer](https://www.zhihu.com/people/mo-chen-42-54)<br/>
#### CSDN：[南浔Pyer](https://blog.csdn.net/qq_45538469)<br/>
#### 个人网站：[DL小站](https://www.idalei.top/)<br/>
#### GitHub：[LeoWang91](https://github.com/LeoWang91)<br/>
