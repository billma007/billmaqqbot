# ✨✨✨BillMa QQ Bot✨✨✨

一个十分~~简陋~~简洁的QQ机器人。不需要Nonebot或者Nonebot2的封装。

由go-cqhttp强力驱动。

## 优点

- 不需要任何机器人框架的封装(~~特指Nonebot~~),语言简单易懂，小白也能看懂(~~毕竟作者本人也是小白~~)
- 无需调试，开箱即用
- 日志清晰，颜色鲜明
- 完全兼容OneBot标准
- 有很清晰的管理员和黑名单体系，且可以远程管理黑名单和管理员
- 可以自由规定禁忌字和手机型号设置
- 可以设置和过滤指定群和私聊、频道消息
- 可以设置指定IP，端口
- ~~很沙雕~~

## 快速食用（Release版本）🍔

#### 1.下载go-cqhttp和本程序

**go-cqhttp**的windows[下载地址](https://github.com/Mrs4s/go-cqhttp/releases/download/v1.0.0-rc1/go-cqhttp_windows_amd64.exe)或者[镜像下载地址](https://ghproxy.com/https://github.com/Mrs4s/go-cqhttp/releases/download/v1.0.0-rc1/go-cqhttp_windows_amd64.exe)

**billmaqqbot**的windows [下载地址](https://github.com/billma007/billmaqqbot/releases/)

#### 2.配置go-cqhttp

**新建一个文件夹，然后把该exe放进去** ，双击exe，选择 `HTTP`，释放相关文件。点击 `config.yml`(右击记事本打开即可),将以下信息原样复制到该文件# go-cqhttp 默认配置文件

```yaml

account: # 账号相关
  uin: # QQ账号(填写的账号一定要与冒号空一格！！！)
  password: '' # 密码为空时使用扫码登录（填写的密码一定要填在单引号里面！！！）
  encrypt: false  # 是否开启密码加密
  status: 0      # 在线状态 请参考 https://docs.go-cqhttp.org/guide/config.html#在线状态
  relogin: # 重连设置
    delay: 3   # 首次重连延迟, 单位秒
    interval: 3   # 重连间隔
    max-times: 0  # 最大重连次数, 0为无限制

  # 是否使用服务器下发的新地址进行重连
  # 注意, 此设置可能导致在海外服务器上连接情况更差
  use-sso-address: true
  # 是否允许发送临时会话消息
  allow-temp-session: false

heartbeat:
  # 心跳频率, 单位秒
  # -1 为关闭心跳
  interval: 5

message:
  # 上报数据类型
  # 可选: string,array
  post-format: string
  # 是否忽略无效的CQ码, 如果为假将原样发送
  ignore-invalid-cqcode: false
  # 是否强制分片发送消息
  # 分片发送将会带来更快的速度
  # 但是兼容性会有些问题
  force-fragment: false
  # 是否将url分片发送
  fix-url: false
  # 下载图片等请求网络代理
  proxy-rewrite: ''
  # 是否上报自身消息
  report-self-message: false
  # 移除服务端的Reply附带的At
  remove-reply-at: false
  # 为Reply附加更多信息
  extra-reply-data: false
  # 跳过 Mime 扫描, 忽略错误数据
  skip-mime-scan: false

output:
  # 日志等级 trace,debug,info,warn,error
  log-level: warn
  # 日志时效 单位天. 超过这个时间之前的日志将会被自动删除. 设置为 0 表示永久保留.
  log-aging: 15
  # 是否在每次启动时强制创建全新的文件储存日志. 为 false 的情况下将会在上次启动时创建的日志文件续写
  log-force-new: true
  # 是否启用日志颜色
  log-colorful: true
  # 是否启用 DEBUG
  debug: false # 开启调试模式

# 默认中间件锚点
default-middlewares: &default
  # 访问密钥, 强烈推荐在公网的服务器设置
  access-token: ''
  # 事件过滤器文件目录
  filter: 'filter.json'
  # API限速设置
  # 该设置为全局生效
  # 原 cqhttp 虽然启用了 rate_limit 后缀, 但是基本没插件适配
  # 目前该限速设置为令牌桶算法, 请参考:
  # https://baike.baidu.com/item/%E4%BB%A4%E7%89%8C%E6%A1%B6%E7%AE%97%E6%B3%95/6597000?fr=aladdin
  rate-limit:
    enabled: false # 是否启用限速
    frequency: 1  # 令牌回复频率, 单位秒
    bucket: 1     # 令牌桶大小

database: # 数据库相关设置
  leveldb:
    # 是否启用内置leveldb数据库
    # 启用将会增加10-20MB的内存占用和一定的磁盘空间
    # 关闭将无法使用 撤回 回复 get_msg 等上下文相关功能
    enable: true

  # 媒体文件缓存， 删除此项则使用缓存文件(旧版行为)
  cache:
    image: data/image.db
    video: data/video.db

# 连接服务列表
servers:
  # HTTP 通信设置
  - http:
      # 是否关闭正向HTTP服务器
      disabled: false
      # 服务端监听地址，用来收QQ信息，可自己设置其它地址
      host: 127.0.0.1
      # 服务端监听端口，用来收QQ信息，可自己设置其它端口
      port: 5700
      # 反向HTTP超时时间, 单位秒
      # 最小值为5，小于5将会忽略本项设置
      timeout: 16
      middlewares:
        <<: *default # 引用默认中间件
      # 反向HTTP POST地址列表
      post:
        - url:  'http://127.0.0.1:8000/' # 这个url用来发送信息，可自己设置其它地址
          secret: ''           # 密钥不要写，就这样空着



```

随后创建文件 `filter.json`.在里面编辑以下内容：

```json
{
    ".or":[{
            "message_type": "guild",
            "guild_id": {
                ".in": [
                    	21212121202020202,
			23288238283828283,
			39293923923928181
                ]
            }   
        }
        ,
        {
            "message_type":"group",
            "group_id":{
                ".in":[
                  	273727372,
                   	232323233,
			293929392
                ]
            }

        }
        ,
        {
            "message_type":"private"
        }
    ]
}
```

##### filer.json详解

这是一个消息过滤器。如果你有json的相关知识，可以[前往go-cqhttp官网](https://docs.go-cqhttp.org/guide/eventfilter.html)查看部分指令的进阶语法。

第一个 `.in`里面填写你想要处理信息的频道ID。如果你不需要，把实例数字删掉即可

第二个 `.in`里面填写你想要处理信息的群号码。如果你不需要，把实例数字删掉即可。

第三个 `private`表示接受私人信息。如果你不需要，删掉即可。

[点击这里了解更多json语法](https://www.runoob.com/json/json-tutorial.html)

#### 配置该程序的配置文件

首先点击 `billbot.exe`,会释放三个文件：

- `botstart.bat`
- `force.bat`
- `settings.json`

首先打开 `force.json`,在superadmin里面填上自己的QQ（**全程在英文状态下输入！全程在英文状态下输入！全程在英文状态下输入！**），要打双引号。**多个QQ要有*****英文半角逗号*** 隔开。**普通管理员和黑名单成员可以使用bot指令远程修改**

随后打开 `settings.json`，一般情况下 `ip,send,listen`选项无需修改，如果出现占用端口的情况可以修改。

group里面填入需要处理的群号，需要用**英文半角括号**隔开

guild里面填入一个list，list[0]为频道ID，list[1]为子频道消息。例如以下实例：

```json
"guild"  : [
["10264721650848156","5682529"],
["10202019392939293","3948382"],
["10201938382939484","29382838"]
],
```

以上指令的意思是：接收三个子频道的消息：

- 频道ID为"10264721650848156",子频道ID为"5682529"的消息
- 频道ID为"10202019392939293",子频道ID为"3948382"的消息
- 频道ID为"10201938382939484",子频道ID为"2382838"的消息

private语法同group。特别的，如果你希望接受所有人发过来的信息，把这一行改成：

```json
"private": ["all"],
```

即可。

随后使用device里显示在线状态。iPhone13.2代表iPhone12。有时候用不了这功能。

taboo里面可以填写禁忌字。如果用户输入含有这个列表里面的关键字，就会回复“含有关键词”。

随后，先点击cqhttp.bat（由go-cqhttp生成），再**点击botstart.bat（直接点击exe可能会出现一些错误），即可开始。**

## 快速食用（Python版）🧶

强烈推荐使用vscode来管理本机器人所需的源代码。

```
git clone https://github.com/billma007/billmaqqbot
cd billmaqqbot
pip install -r requirements.txt
# 此处需要先配置go-cqhttp
python3 main.py
```

### 小白食用（windows版）

#### 1.下载go-cqhttp

windows[下载地址](https://github.com/Mrs4s/go-cqhttp/releases/download/v1.0.0-rc1/go-cqhttp_windows_amd64.exe)或者[镜像下载地址](https://ghproxy.com/https://github.com/Mrs4s/go-cqhttp/releases/download/v1.0.0-rc1/go-cqhttp_windows_amd64.exe)

#### 2.配置go-cqhttp

**新建一个文件夹，然后把该exe放进去** ，双击exe，选择 `HTTP`，释放相关文件。点击 `config.yml`(右击记事本打开即可),将以下信息原样复制到该文件：

```yaml
# go-cqhttp 默认配置文件

account: # 账号相关
  uin: # QQ账号(填写的账号一定要与冒号空一格！！！)
  password: '' # 密码为空时使用扫码登录（填写的密码一定要填在单引号里面！！！）
  encrypt: false  # 是否开启密码加密
  status: 0      # 在线状态 请参考 https://docs.go-cqhttp.org/guide/config.html#在线状态
  relogin: # 重连设置
    delay: 3   # 首次重连延迟, 单位秒
    interval: 3   # 重连间隔
    max-times: 0  # 最大重连次数, 0为无限制

  # 是否使用服务器下发的新地址进行重连
  # 注意, 此设置可能导致在海外服务器上连接情况更差
  use-sso-address: true
  # 是否允许发送临时会话消息
  allow-temp-session: false

heartbeat:
  # 心跳频率, 单位秒
  # -1 为关闭心跳
  interval: 5

message:
  # 上报数据类型
  # 可选: string,array
  post-format: string
  # 是否忽略无效的CQ码, 如果为假将原样发送
  ignore-invalid-cqcode: false
  # 是否强制分片发送消息
  # 分片发送将会带来更快的速度
  # 但是兼容性会有些问题
  force-fragment: false
  # 是否将url分片发送
  fix-url: false
  # 下载图片等请求网络代理
  proxy-rewrite: ''
  # 是否上报自身消息
  report-self-message: false
  # 移除服务端的Reply附带的At
  remove-reply-at: false
  # 为Reply附加更多信息
  extra-reply-data: false
  # 跳过 Mime 扫描, 忽略错误数据
  skip-mime-scan: false

output:
  # 日志等级 trace,debug,info,warn,error
  log-level: warn
  # 日志时效 单位天. 超过这个时间之前的日志将会被自动删除. 设置为 0 表示永久保留.
  log-aging: 15
  # 是否在每次启动时强制创建全新的文件储存日志. 为 false 的情况下将会在上次启动时创建的日志文件续写
  log-force-new: true
  # 是否启用日志颜色
  log-colorful: true
  # 是否启用 DEBUG
  debug: false # 开启调试模式

# 默认中间件锚点
default-middlewares: &default
  # 访问密钥, 强烈推荐在公网的服务器设置
  access-token: ''
  # 事件过滤器文件目录
  filter: 'filter.json'
  # API限速设置
  # 该设置为全局生效
  # 原 cqhttp 虽然启用了 rate_limit 后缀, 但是基本没插件适配
  # 目前该限速设置为令牌桶算法, 请参考:
  # https://baike.baidu.com/item/%E4%BB%A4%E7%89%8C%E6%A1%B6%E7%AE%97%E6%B3%95/6597000?fr=aladdin
  rate-limit:
    enabled: false # 是否启用限速
    frequency: 1  # 令牌回复频率, 单位秒
    bucket: 1     # 令牌桶大小

database: # 数据库相关设置
  leveldb:
    # 是否启用内置leveldb数据库
    # 启用将会增加10-20MB的内存占用和一定的磁盘空间
    # 关闭将无法使用 撤回 回复 get_msg 等上下文相关功能
    enable: true

  # 媒体文件缓存， 删除此项则使用缓存文件(旧版行为)
  cache:
    image: data/image.db
    video: data/video.db

# 连接服务列表
servers:
  # HTTP 通信设置
  - http:
      # 是否关闭正向HTTP服务器
      disabled: false
      # 服务端监听地址，用来收QQ信息，可自己设置其它地址
      host: 127.0.0.1
      # 服务端监听端口，用来收QQ信息，可自己设置其它端口
      port: 5700
      # 反向HTTP超时时间, 单位秒
      # 最小值为5，小于5将会忽略本项设置
      timeout: 16
      middlewares:
        <<: *default # 引用默认中间件
      # 反向HTTP POST地址列表
      post:
        - url:  'http://127.0.0.1:8000/' # 这个url用来发送信息，可自己设置其它地址
          secret: ''           # 密钥不要写，就这样空着


```

#号后面的注释无需删除。需要注意，**每个冒号和后面的内容都需要一个空格！**

以上只需修改QQ账号和密码即可。

随后创建文件 `filter.json`,在里面填写以下内容：

```json
{
    ".or":[{
            "message_type": "guild",
            "guild_id": {
                ".in": [
                    	21212121202020202,
			23288238283828283,
			39293923923928181
                ]
            }   
        }
        ,
        {
            "message_type":"group",
            "group_id":{
                ".in":[
                  	273727372,
                   	232323233,
			293929392
                ]
            }

        }
        ,
        {
            "message_type":"private"
        }
    ]
}
```

##### filer.json详解

这是一个消息过滤器。如果你有json的相关知识，可以[前往go-cqhttp官网](https://docs.go-cqhttp.org/guide/eventfilter.html)查看部分指令的进阶语法。

第一个 `.in`里面填写你想要处理信息的频道ID。如果你不需要，把实例数字删掉即可

第二个 `.in`里面填写你想要处理信息的群号码。如果你不需要，把实例数字删掉即可。

第三个 `private`表示接受私人信息。如果你不需要，删掉即可。

[点击这里了解更多json语法](https://www.runoob.com/json/json-tutorial.html)

## 指令👍

- `.bot arknights`明日方舟模拟抽卡
- `.bot rc` or `.bot 事件鉴定`事件鉴定，指数越大概率越大
- `.bot jrrp`  今日人品
- `.bot 人生重开`  人生重开模拟器，不支持自选天赋
- `.bot 下载音乐`  加上歌曲名称，自动解析腾讯，网易，咪咕三家音乐网站下载直链、（支持vip）
- `.bot 毒鸡汤`    来一句毒鸡汤
- `.bot 狗屁不通`  随机生成一篇狗屁不通小短文
- `.bot 疫情查询`+一个省名（例如江苏省），查询该省疫情（暂不支持市级）
- 此外，`.bot`  后面直接加句子可以获得聊天功能

## 管理指令🎉

首先需要在force.json里的“superadmin”中将自己QQ填上。随后就可以用自己的QQ号使用远程指令操作管理。

- `.bot set admin add xxxxx`添加xxxxx为普通管理员（无法解除超级管理员）
- `.bot set admin remove xxxxx`取消xxxxx为管理员（无法解除超级管理员）
- `.bot set admin search` 输出所有管理员和超级管理员
- `.bot set blacklist add xxxxx`将xxxxx列入黑名单
- `.bot set blacklist remove xxxxx`将xxxxx移除黑名单
- `.bot set blacklist search`列出所有黑名单成员

### 开发中的指令

- `.bot set restart`重启机器人

## 环境🎶

本机器人在以下环境测试通过：

- windows系统
  - windows10
  - python 3.8.5-64bits
  - Visual Studio Code 2022
  - go-cqhttp windows_amd64

## 使用的开源库❤

我只是一个高中牲，很菜，没多少技术，因此~~魔改~~借鉴了很多大佬的代码。特将这些开源库列出以示感谢：

| 开源库                                                                                                                                                                           | 用途                                 | 开源许可证                                                                       |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ | -------------------------------------------------------------------------------- |
| [menzi11/BullshitGenerator: Needs to generate some texts to test if my GUI rendering codes good or not. so I made this. (github.com)](https://github.com/menzi11/BullshitGenerator) | 生成狗屁不通文章                     | "Anti 996" License                                                               |
| [CharlesPikachu/musicdl: Musicdl: A lightweight music downloader written by pure python. (github.com)](https://github.com/CharlesPikachu/musicdl)                                   | 原用途为下载音乐，魔改为直接提取直链 | [Apache-2.0 license](https://github.com/CharlesPikachu/musicdl/blob/master/LICENSE) |
| [cc004/lifeRestart-py: lifeRestart game in python (github.com)](https://github.com/cc004/lifeRestart-py)                                                                            | 人生重开，但是阉割了自选天赋 的功能  | [AGPL-3.0 license](https://github.com/cc004/lifeRestart-py/blob/main/LICENSE)       |

## 进阶使用😘

本仓库含有以下主要文件：

- `main.py`主函数
- `receive.py`接收信息
- `send_msg.py`发送消息
- `bot_blacklist.py`黑名单和管理员管理
- `bot_changename.py`修改群名片
- `bot_debug.py`调试工具

也有以下静态文件：

- `force.json`黑名单和管理员名单
- `error.json`错误代码
- `musicdl.log`下载音乐的配置文件
- `dujitang.json`毒鸡汤存放处

还有以下插件：

- `bot_plugin_covid.py` 疫情查询
- `bot_plugin_aitalk.py 只能聊天`
- `bot_plugin_dujitang.py`毒鸡汤
- `bot_plugin_goupibutong.py`生成狗屁不通文章
- `bot_plugin_jrrp.py侧人品`
- `bot_plugin_liferestart.py`人生重开
- `bot_plugin_musicdown.py`  下载音乐
- `bot_plugin_check.py 事件鉴定`

## 更新日志

- `2022/4/12` 开始编写
- `2022/4/18 0.1.92alpha` 具有自然语言处理
- `2022/4/21 0.1.98alpha` ~~瞎~~写了一个今日人品的插件
- `2022/4/22 0.1.113alpha` 新增狗屁不通功能
- `2022/4/24 0.3.34alpha` 新增管理系统，新增音乐下载功能，新增新冠查询功能
- `2022/4/26 1.0.0 Beta` 开放频道功能内测，优化代码结构
- `2022/4/26 0.6.39 alpha`新增人生重开
- `2022/4/27 0.8.0 alpha`新增事件鉴定和毒鸡汤
- `2022/5/2 1.0.0-rc2` 重构代码，优化结构，兼容性更强
- `2022/5/4 1.0.0-rc4`成功适配群聊功能
- `2022/5/5 1.0.0-rc5`运算逻辑优化
- `2022/5/6 1.1.1 alpha`新增管理模式，新增成员权限等级
- `2022/5/7 1.1.3 alpha`优化了权限系统
- `2022/5/8 1.2.0 alpha`新增settings.json，管理设置更加方便了
- `2022/5/9 1.0.0-rc12 Release`发布，修复大量bug


## 关于作者😁

江苏省苏州市的一个普通高中牲，一个因为~玩电脑被学校处分~在省赛就被刷下来的信息学奥林匹克竞赛选手，热爱编程，但不喜欢前端。

欢迎通过以下联系方式与我探讨信息竞赛、博客搭建、学术讨论以及扯皮：

* QQ:36937975
* Twitter:@billma6688
* Facebook/Instagram:billma007
* CodeForces/USACO/AtCoder:billma007(~别看我很拉的~不常用)
* Email:[maboning237103015@163.com](mailto:maboning237103015@163.com)

## 推广：我的博客🤞

[欢迎光临！](https://billma.top/)
