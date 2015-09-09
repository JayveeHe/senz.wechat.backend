# coding=utf-8
import re
import sys
from urllib import quote
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
                 u'test': user_login}
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


def user_login(content_dict={}):
    tousername = content_dict["FromUserName"]
    fromusername = content_dict["ToUserName"]
    re_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?' \
             'appid=%s' \
             '&redirect_uri=%s' \
             '&response_type=code' \
             '&scope=%s' \
             '&state=STATE#wechat_redirect' % \
             ('wx77081de86b8e6232',quote('http://120.27.30.239:80/login'), 'snsapi_userinfo')
    #re_url = quote(re_url1)
    return WeixinUtils.make_singletext(tousername, fromusername,
                                       "请访问%s" % re_url)

    # print check_task({"FromUserName": "123123", "ToUserName": "454564", "Content": "/帮助 查看"})
