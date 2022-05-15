def HELP():
    return """欢迎您使用马哥机器人！
本机器人使用文档：https://billma.top/qqbot
源代码地址： https://github.com/billma007/billmaqqbot
exe下载地址：https://github.com/billma007/billmaqqbot/releases
如果您对指令有疑问，可前往https://billma.top/qqbot/help.html 查看指令的完整版
本项目遵守GNU GPL v3.0开源版权协议
==================
本机器人有以下通用功能：
.bot rc 一个事件：事件鉴定
.bot jrrp (可加人名)：测某人今日人品(不加人名就是测自己)
.bot arknights (可加数字)：方舟模拟寻访(不加数字爆率为2%，加数字即代表爆率)
.bot 人生重开 ：模拟一次人生重开
.bot 毒鸡汤：随机来一句毒鸡汤
.bot 下载音乐 (歌名):获取音乐下载链接，支持会员
.bot history-today :获取历史上的今天
.bot 狗屁不通 (一个名词)：生成该名词的狗屁不通文章
===================
机器人还有部分查询功能，支持查询以下内容：
查询天气预报信息，示例：.bot 天气 深圳
手机、IP地址归属，示例：.bot 归属 手机或IP
邮政编码及地区查询：.bot 邮编 514000
计算简单的算术，示例：.bot 计算 15+13
查询成语介绍，示例：.bot 成语 一心一意
按歌曲名称查询歌词，.bot 示例：歌词 歌曲名称
中译英、英译中，示例：.bot 翻译 i love you
查询星座今日运势，示例：.bot 星座 天秤座
查询星座介绍请直接发送：.bot 天秤座
汉字五笔拼音笔画查询示例：.bot 礡字
想看笑话，请直接发送：.bot 笑话"
==================
特别地，在群聊里面还支持积分系统，具体如下：
.bot signin [options] ....
options可替换成：

qd:每日签到
----------
db (加赌注大小)：进行du博
例如 ：.bot signin db 155
----------
guess (四个0-9的整数，后加空格，再加竞猜金额):猜数字
example:.bot signin guess 1 3 5 6 10000
----------
search:查询自己的积分
=================
此外，以下积分指令只支持1,2级管理员操作：
.bot signin admin check 12345:查询12345的积分
.bot signin admin add 12345 1000:给12345增加1000个积分
.bot signin admin remove 12345 100:给12345移除100积分
=================
此外，管理员可以使用以下全局指令管理黑名单：
.bot set blacklist add/delete 12345:将12345加入/移除黑名单
.bot set blacklist search:输出所有在黑名单中的成员
.bit set taboo add/delete 傻X:将“傻X”设置/移除禁忌词列表
=================
超级管理员可以远程管理普通管理员，超级管理员只能在本地设置：
.bot set admin add/delete 12345:将12345设为/移除普通管理员
.bot set admin search:输出所有的管理员
"""
