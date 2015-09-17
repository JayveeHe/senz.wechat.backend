# coding=utf-8
import json
import re
import sys
from urllib import quote
import requests
import music_utils

import WeixinUtils

__author__ = 'Jayvee'

reload(sys)
sys.setdefaultencoding('utf8')


def check_task(content_dict={}):
    """
    对用户提交的内容进行统一的识别，并给出相应的回复
    :param content_dict:
    :return:
    """
    func_dict = {u'帮助': get_commandmenu, u'help': get_commandmenu,
                 u'听歌': get_music, 'song': get_music, u's': get_music,
                 u'test': tag_demo}
    text = content_dict["Content"]
    tousername = content_dict["FromUserName"]
    fromusername = content_dict["ToUserName"]
    if text[0] == "/" and len(text) > 1:
        # 进入功能模式，首先获取命令
        commd = re.compile(r'/[^ ]*').match(text).group()
        commd = commd[1:]
        commd_content = re.compile(r'/[^ ]* ').sub("", text)
        # print commd
        # print commd_content
        func = func_dict.get(commd)
        if func is not None:
            # print "function: %s" % commd
            # logger.info('%s sends %s, and resp success' % (tousername, text))
            return func(content_dict)
        else:
            # logger.info('%s sends %s, and resp fail' % (tousername, text))
            return get_error_resp(content_dict)
    else:
        # logger.info('%s sends %s, and resp default' % (tousername, text))
        return get_defaultresp(content_dict)


def get_defaultresp(content_dict={}):
    """
    返回指令列表
    :param content_dict:
    :return:
    """
    tousername = content_dict["FromUserName"]
    fromusername = content_dict["ToUserName"]
    reply = "你好，可以使用 “/”前缀+短语 进行指令操作，例如：/帮助"
    return WeixinUtils.make_singletext(tousername, fromusername, reply)


def get_commandmenu(content_dict={}):
    """
    返回指令列表
    :param content_dict:
    :return:
    """
    tousername = content_dict["FromUserName"]
    fromusername = content_dict["ToUserName"]
    str_commandmenu = "/帮助或/help：查看所有指令"
    return WeixinUtils.make_singletext(tousername, fromusername, str_commandmenu)


def get_music(content_dict={}):
    """
    返回云音乐爬取结果
    :param content_dict:
    :return:
    """
    text = content_dict["Content"]
    tousername = content_dict["FromUserName"]
    fromusername = content_dict["ToUserName"]
    songname = re.compile(r'/[^ ]* ').sub("", text)
    if len(songname) > 0 and songname != "/听歌":
        songlist = music_utils.get_searchlist(songname, 5)
        if songlist != None:
            return WeixinUtils.make_news(songlist, tousername, fromusername)
        else:
            return WeixinUtils.make_singletext(tousername, fromusername, "未找到相应的歌曲！")
    else:
        return WeixinUtils.make_singletext(tousername, fromusername, "请输入歌曲名！")


def get_error_resp(content_dict={}):
    """
    输入的指令以-开头，但是没有找到相应的指令关键字
    :param content_dict:
    :return:
    """
    tousername = content_dict["FromUserName"]
    fromusername = content_dict["ToUserName"]
    return WeixinUtils.make_singletext(tousername, fromusername, "指令有误,输入 /帮助 查看指令列表")


# todo senz demo
def tag_demo(content_dict):
    base_url = ''
    text = content_dict["Content"]
    tousername = content_dict["FromUserName"]
    fromusername = content_dict["ToUserName"]
    article_list = json.loads(requests.get(base_url + '/wechat_articles').content)
    a_url_map = {
        'tfboy': 'http://mp.weixin.qq.com/s?__biz=MzI1NTAxMTQwNQ==&mid=209956548&idx=1&sn=cc52b85072fefa296a7c5cb82dc62d34&scene=0&key=dffc561732c22651ddec47d91a219c794d0b204ef1258177ff8c11b3a77ba4188a6f8460a018e3f3e4bce4f5d8842b1f&ascene=0&uin=NDEyNTkyMzIw&devicetype=iMac+MacBookAir7%2C2+OSX+OSX+10.10.5+build(14F27)&version=11020201&pass_ticket=TzKtzXhA0l8eQjH%2F6GQzDu0eUG3q2CfimIMMueJ6COMF%2FlRyv63DyQgfdczmq0lj',
        'media': 'http://mp.weixin.qq.com/s?__biz=MzI1NTAxMTQwNQ==&mid=209956583&idx=1&sn=136dd5735898adb03dc017af6a4ad1a5#rd',
        'sportclass': 'http://mp.weixin.qq.com/s?__biz=MzI1NTAxMTQwNQ==&mid=209956618&idx=1&sn=34d1f00231abc79bb6d5e530e681f8f2#rd',
        'prod': 'http://mp.weixin.qq.com/s?__biz=MzI1NTAxMTQwNQ==&mid=209956649&idx=1&sn=f25062f29eb6bc779bf1b15a3690603c#rd',
        'wenzhou': 'http://mp.weixin.qq.com/s?__biz=MzI1NTAxMTQwNQ==&mid=209956662&idx=1&sn=da827726c75655d826be3c348bc88549#rd',
        'qiuyi': 'http://mp.weixin.qq.com/s?__biz=MzI1NTAxMTQwNQ==&mid=209956662&idx=1&sn=da827726c75655d826be3c348bc88549#rd'}
    news_list = [WeixinUtils.NewsItem(a_url_map['tfboy'], 'TFBOYS为什么这样红',
                                      'http://mmbiz.qpic.cn/mmbiz/SWL3EF8DbcxQPnJYStuemOSNdvf8ia7gxFIu394xfL2xmgqVWQxutZZVXWYJpU2DdXM3Z5Huu8sTgia1icYZbtSBw/640?wx_fmt=jpeg&wxfrom=5'),
                 WeixinUtils.NewsItem(a_url_map['media'], '注意力时代不可不知的新媒体8人',
                                      'http://mmbiz.qpic.cn/mmbiz/SWL3EF8DbcxQPnJYStuemOSNdvf8ia7gxFIu394xfL2xmgqVWQxutZZVXWYJpU2DdXM3Z5Huu8sTgia1icYZbtSBw/640?wx_fmt=jpeg&wxfrom=5'),
                 WeixinUtils.NewsItem(a_url_map['sportclass'], '体育与阶层',
                                      'http://mmbiz.qpic.cn/mmbiz/SWL3EF8DbcxQPnJYStuemOSNdvf8ia7gxFIu394xfL2xmgqVWQxutZZVXWYJpU2DdXM3Z5Huu8sTgia1icYZbtSBw/640?wx_fmt=jpeg&wxfrom=5'),
                 WeixinUtils.NewsItem(a_url_map['prod'], '无人见过我们真正的产品',
                                      'http://mmbiz.qpic.cn/mmbiz/SWL3EF8DbcxQPnJYStuemOSNdvf8ia7gxFIu394xfL2xmgqVWQxutZZVXWYJpU2DdXM3Z5Huu8sTgia1icYZbtSBw/640?wx_fmt=jpeg&wxfrom=5'),
                 WeixinUtils.NewsItem(a_url_map['wenzhou'], '温州话能成为军事密码么',
                                      'http://mmbiz.qpic.cn/mmbiz/SWL3EF8DbcxQPnJYStuemOSNdvf8ia7gxFIu394xfL2xmgqVWQxutZZVXWYJpU2DdXM3Z5Huu8sTgia1icYZbtSBw/640?wx_fmt=jpeg&wxfrom=5'),
                 WeixinUtils.NewsItem(a_url_map['qiuyi'], '球衣往事',
                                      'http://mmbiz.qpic.cn/mmbiz/SWL3EF8DbcxQPnJYStuemOSNdvf8ia7gxFIu394xfL2xmgqVWQxutZZVXWYJpU2DdXM3Z5Huu8sTgia1icYZbtSBw/640?wx_fmt=jpeg&wxfrom=5'),
                 ]

    # songname = re.compile(r'/[^ ]* ').sub("", text)
    # if len(songname) > 0 and songname != "/听歌":
    #     songlist = music_utils.get_searchlist(songname, 5)
    #     if songlist != None:
    return WeixinUtils.make_news(news_list, tousername, fromusername)
    #     else:
    #         return WeixinUtils.make_singletext(tousername, fromusername, "未找到相应的歌曲！")
    # else:
    #     return WeixinUtils.make_singletext(tousername, fromusername, "请输入歌曲名！")


def user_login(content_dict={}):
    tousername = content_dict["FromUserName"]
    fromusername = content_dict["ToUserName"]
    re_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?' \
             'appid=%s' \
             '&redirect_uri=%s' \
             '&response_type=code' \
             '&scope=%s' \
             '&state=STATE#wechat_redirect' % \
             ('wx77081de86b8e6232', quote('http://120.27.30.239:80/login'), 'snsapi_userinfo')
    # re_url = quote(re_url1)
    return WeixinUtils.make_singletext(tousername, fromusername,
                                       "请访问%s" % re_url)

    # print check_task({"FromUserName": "123123", "ToUserName": "454564", "Content": "/帮助 查看"})
