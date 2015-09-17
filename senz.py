# encoding:utf8
import logging
import sys
import WeixinUtils
import task_manager

reload(sys)
sys.setdefaultencoding('utf8')
__author__ = 'Jayvee'

from flask import Flask, request, make_response
import hashlib
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# lh = logentries.LogentriesHandler(token_config.LOGENTRIES_TOKEN)
# fm = logging.Formatter('%(asctime)s : %(levelname)s, %(message)s',
#                        '%a %b %d %H:%M:%S %Y')
# lh.setFormatter(fm)
# logger.addHandler(lh)
app = Flask(__name__)


@app.route('/senz-wechat', methods=['GET', 'POST'])
def jiabei():
    if request.method == 'GET':
        if len(request.args) > 3:
            temparr = []
            token = "xiaosenz"
            signature = request.args["signature"]
            timestamp = request.args["timestamp"]
            nonce = request.args["nonce"]
            echostr = request.args["echostr"]
            temparr.append(token)
            temparr.append(timestamp)
            temparr.append(nonce)
            temparr.sort()
            newstr = "".join(temparr)
            sha1str = hashlib.sha1(newstr)
            temp = sha1str.hexdigest()
            if signature == temp:
                return echostr
            else:
                return "认证失败，不是微信服务器的请求！"
        else:
            return "你请求的方法是：" + request.method
    else:  # POST
        xmldict = WeixinUtils.recv_msg(request.data)
        if xmldict["MsgType"] == "event":
            if xmldict["Event"] == "subscribe":
                reply = WeixinUtils.make_singletext(xmldict["FromUserName"],
                                                    xmldict["ToUserName"],
                                                    "欢迎关注Senz情境技术，希望能与你交流更多有趣的想法！"
                                                    "\n输入/帮助 查看相关操作指令。祝愉快！")
            else:
                reply = ""
        else:
            reply = task_manager.check_task(xmldict)
        response = make_response(reply)
        response.content_type = 'application/xml'
        return response


@app.route('/login/', methods=['GET'])
def login_and_have_fun():
    code = request.args.get('code')
    state = request.args.get('state')
    return 'code=%s, state=%s'%(code,state)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
