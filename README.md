# python+selenium实现自动订舱

[TOC]

## 0x01前言+准备工具

最近重操旧业想写点爬虫，感受一下刚上大学用python敲出hello world的那段时光，重温俺那逝去的青春呐( ╯□╰ )

github地址 ：https://github.com/iznilul/magicargoSpider

浏览器：chrome91.0及其驱动

python3.7+selenium

基于订舱网站 http://www.magicargo.com/#/

## 0x02 需求流程

这次的分析是基于登录账户-》站到站查询-》班列订舱-》填写信息-》下单

打开主页

![http://image.radcircle.love/7e55463e3ebc420d8e4285ca2bee5406](http://image.radcircle.love/7e55463e3ebc420d8e4285ca2bee5406)

点击查询可以看到班列信息，点击订舱

![http://image.radcircle.love/e7ca27c83abb4f2c9f5265c4845af1c9](http://image.radcircle.love/e7ca27c83abb4f2c9f5265c4845af1c9)

在这个页面填上一些货物信息，下单

![http://image.radcircle.love/af1d42d5cb28410c9586d8411ad77a8b](http://image.radcircle.love/af1d42d5cb28410c9586d8411ad77a8b)

会有一个验证码，验证通过即可下单

## 0x03 分析

根据这个需求决定写一个自动化脚本比较好，所以采用浏览器模拟请求的方式，动态调试方法

首先在桌面上新建立一个chrome快捷方式，然后再硬盘里准备一个空文件夹

打开快捷方式属性，在后面加上

--remote-debugging-port=5003 --user-data-dir="D:\python\pySelenium"

标识5003为浏览器的调试端口，可以通过访问这个端口控制浏览器

python代码

```python
self.options = webdriver.ChromeOptions()
self.options.add_experimental_option("debuggerAddress", "127.0.0.1:5003")      #调试方法启动浏览器
self.driver = webdriver.Chrome(options=self.options)
```

这样就可以，动态的调试浏览器，不用像以前那样用selenium每次运行都得重启啦

### 登录

登录可以设置cookies解决，而且因为是用浏览器请求，只要在第一次登录网站的时候登录一次，浏览器就可以保存cookies到本地

![http://image.radcircle.love/1547a50ca2d64f6bbb59bbf976515b5d](http://image.radcircle.love/1547a50ca2d64f6bbb59bbf976515b5d)

而且保质期有一个月，一个月内只要再次登录就能继续延长

为了保险起见我还是把cookies的一些函数写上了，只不过没有调用

### 查询

这一部分比较简单，定位四个元素模拟填入和点击即可

![http://image.radcircle.love/362b4e0a605944889f3a187575a30107](http://image.radcircle.love/362b4e0a605944889f3a187575a30107)

需要注意的点是起始地和目的地需要先**选中元素-》填入部分字段-》再根据提示选择字段**，源代码中有具体步骤

### 订舱&填写消息

点击查询之后回有一个xhr请求耗时比较长需要sleep一会

填写消息时也是最后一个确认checkbox类型需要用js脚本模拟点击

其他都是比较基础的操作，就不一一赘述了

### 下单&&滑动验证

验证码这里需要仔细分析一下

点击下单之后会弹出一张验证码

![http://image.radcircle.love/af1d42d5cb28410c9586d8411ad77a8b](http://image.radcircle.love/af1d42d5cb28410c9586d8411ad77a8b)

这种滑动验证一般采用的方法是对比两张图片，计算图像左侧到拼图缺口的距离，然后模拟拉取操作

#### 坑一

首先我们需要得到两张图片，一张背景图一张有缺口的图

可是我发现网页元素上只有这一张缺口图，背景图藏在了network选项卡的静态资源请求记录里( ╯□╰ )

![http://image.radcircle.love/f899edc79fca4c13a2b4e097fe8b2920](http://image.radcircle.love/f899edc79fca4c13a2b4e097fe8b2920)

网页元素缺口可以用截图的方式保存到本地

这张藏在network选项卡里的图片只好先获取chrome performance日志记录，然后再把base64转码存储

#### 坑二

仔细对比两张图片那张缺口的截图图片似乎有问题，因为它最上面总有一个没截完整的细细白条

![http://image.radcircle.love/a1c61c62a6414730a89ba8e9c462a6f5](http://image.radcircle.love/a1c61c62a6414730a89ba8e9c462a6f5)

这样两张图片根本不一样，导致无法定位

俺只好用裁剪的方式修改了一下

![http://image.radcircle.love/21892f047bdd436db67117eecd96f49c](http://image.radcircle.love/21892f047bdd436db67117eecd96f49c)

这样就帅多了OvO

然后俺用网上找来的参考代码，结合pillow图像处理的函数，进行了缺图定位和模拟拉取

模拟滑动之后下单完成

## 0x04总结+参考资料

总之还是一个很水的自动化脚本，后续如果需要的话将继续优化

https://cloud.tencent.com/developer/article/1703946

https://www.cnblogs.com/liuhui0308/p/12091810.html

https://www.aneasystone.com/archives/2018/03/python-selenium-geetest-crack.html

