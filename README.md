# 项目
- [github项目](https://github.com/kate0603/danmu_crawler)
## 流程
![](https://cdn.nlark.com/yuque/0/2024/jpeg/745518/1708676513581-b1ea0d74-7daa-4382-97c6-394d3184bf14.jpeg)
### 代理

- 从多个代理服务网站中爬取免费的ip，验证其可用性之后，放入redis。
- 定时调度，验证其可用性；同时redis里的ip数量少于最小值时，触发上一个步骤，补充ip。
- 触发爬虫程序之前，从redis取出一个ip，再次验证可用后，用于request或者websocket的代理。
### 实时弹幕爬虫
采用进程或者协程的方式获取，但因为直播结束时间未知，所以一定时间后关闭（30分钟）。等待事件通知后重新唤起程序。
#### bilibili
采用异步协程，可同时抓取多个房间ID的直播弹幕。

- 获取代理ip，初始化异步协程session(aiohttp.ClientSession)，指定时间关闭协程（asyncio.wait）。
- 初始化房间信息(session.get)
   - 判断直播用户是否登录，若已登录，获取其uid。
   - 获取cookies中的buvid3。
   - 获取房间信息，获取房间ID和房间owner_uid。如果不是直播状态，则不继续。（不再直播时，房间依然存在）。
   - 获取弹幕需要的host_server_list和token。
- 建立websocket长连接（session.ws_connect）， _handler处理不同的消息。
- 备注：
   - SESSDATA填一个已登录账号的cookie。cookie过期时，收到弹幕的用户名会打码，UID会变成0。
#### 抖音
采用进程池，可同时抓取多个webid（非room_id）的直播弹幕。

- 获取代理ip，开启进程池，指定时间关闭进程。
- 初始化房间信息（requests.get）， 获取房间ID等信息。
- 建立websocket长连接（websocket.WebSocketApp().run_forever）。
- 备注：
   - ttwid填一个已登录账号的cookie。cookie过期时，收到弹幕的用户名会打码，UID会变成111111。
# 平台开放API

- [bilibili开放平台](https://openhome.bilibili.com/doc/4/aa909d41-01da-e47e-e64c-f32bc76b8a42)
- [抖音开放平台](https://developer.open-douyin.com/docs/resource/zh-CN/interaction/introduction/capabilities/jierushuoming/hudongshuju/pinglunshuju)
# 参考
## 代理

- [代理池](https://github.com/jhao104/proxy_pool)参考示例
## Bilibili

- 房间号：打开直播间，从url里查看。![image.png](https://cdn.nlark.com/yuque/0/2024/png/745518/1707030505921-6598d1d4-f8e4-4a2d-b097-7749bf456871.png#averageHue=%23cfe3dd&clientId=u6d1a5138-1384-4&from=paste&height=34&id=u8ad289d7&originHeight=43&originWidth=805&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=6612&status=done&style=none&taskId=ud1beea15-b3b4-4497-a74b-6ad03c7ef80&title=&width=644)
- SESSDATA：有该值之后，才能获取真正的用户id和名称。账号登录b站之后，F12打开，找到其中一个请求，查看cookies中的SESSDATA。![image.png](https://cdn.nlark.com/yuque/0/2024/png/745518/1707030591093-bff5e726-2010-4fc3-a595-e6ffa7dbe8ff.png#averageHue=%23dadcd9&clientId=u6d1a5138-1384-4&from=paste&height=183&id=u0c9672fa&originHeight=605&originWidth=1277&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=112351&status=done&style=none&taskId=ua3aaa163-3855-48e4-8c40-04da4218d5a&title=&width=385.4000244140625)
- 查看主播身份码：【[饭饭](https://play-live.bilibili.com/)】首页右下角即可查看。

![image.png](https://cdn.nlark.com/yuque/0/2024/png/745518/1707030677169-a161ecd8-aa61-41a6-b0c3-131e7453203d.png#averageHue=%234f9f9d&clientId=u6d1a5138-1384-4&from=paste&height=178&id=u7262c2b2&originHeight=648&originWidth=1387&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=1463977&status=done&style=none&taskId=u7f310dc2-e2b1-464d-9fc3-aabe344d436&title=&width=381.4000244140625)

- [cookies刷新示例](https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/login/cookie_refresh.md#Python) （待验证）
- [爬虫直播弹幕示例](https://github.com/xfgryujk/blivedm?tab=readme-ov-file)
## 抖音

- [爬虫直播弹幕示例](https://gitee.com/haodong108/dy-barrage-grab#-%E6%8A%96%E9%9F%B3%E5%BC%B9%E5%B9%95%E7%9B%91%E5%90%AC%E5%99%A8)
- [爬虫直播弹幕示例2](https://github.com/Sjj1024/douyin-live?tab=readme-ov-file)
- [弹幕类型说明](https://danmaku-doc.hperfect.cn/zh-cn/douyin/fields_description.html)
   - .判断开始 (Json.取文本 (“common.method”) ＝ “WebcastSocialMessage”)'关注
.判断 (Json.取文本 (“common.method”) ＝ “WebcastChatMessage”)‘弹幕
.判断 (Json.取文本 (“common.method”) ＝ “WebcastLikeMessage”)‘点赞
.判断 (Json.取文本 (“common.method”) ＝ “WebcastGiftMessage”)'礼物
.判断 (Json.取文本 (“common.method”) ＝ “WebcastMemberMessage”) ‘进入直播间
.判断 (Json.取文本 (“common.method”) ＝ “WebcastInRoomBannerMessage”)
.判断 (Json.取文本 (“common.method”) ＝ “WebcastRoomUserSeqMessage”)  ' 榜十 直播间人数
.判断 (Json.取文本 (“common.method”) ＝ “WebcastRoomUserSeqMessage”)  ' 小时榜时时状态
.判断 (Json.取文本 (“common.method”) ＝ “WebcastSunDailyRankMessage”)  ' 全站小时榜时时状态
.判断 (Json.取文本 (“common.method”) ＝ “WebcastFansclubMessage”)  ' 加入粉丝团
.判断 (Json.取文本 (“common.method”) ＝ “WebcastCommonTextMessage”)  ' 为主播加积分
.判断 (Json.取文本 (“common.method”) ＝ “WebcastUpdateFanTicketMessage”)  ' 主播礼物数.判断 (Json.取文本 (“common.method”) ＝ “WebcastCommerceMessage”)  ' 主播小游戏推广信息
- 爬虫时的用户是匿名：cookie中的ttwid需要刷新。
- F12控制台输入获得房间ID![image.png](https://cdn.nlark.com/yuque/0/2024/png/745518/1707184365847-00d01d02-2e63-449d-8493-20394e8b6dca.png#averageHue=%23f9efcc&clientId=ub1f64023-9181-4&from=paste&height=424&id=u199c53c8&originHeight=530&originWidth=894&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=95501&status=done&style=none&taskId=ua040201d-7a73-45cd-8835-b8191d7316f&title=&width=715.2)
# 其他分析产品

- [火烧云数据](https://www.hsydata.com/index?redirect=%2F)：B站、小红书。
- [蝉妈妈](https://www.chanmama.com/)：抖音。
