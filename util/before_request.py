from flask import request
from util.Response import response
from util.operate_token import operate_token
import util.config as config

def before_request():
    if request.path not in config.NOT_CHECK_URL:
        try:
            token_ = request.headers['token']
        except:
            return response(data={'code':40101},msg="无访问权限",status=401)
        res = operate_token.validate_token(token_)
        return res
    else:
        # token_ = request.headers['token']
        res = None
    if res:
        return res