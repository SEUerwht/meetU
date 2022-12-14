from flask import Flask, request
from api.user_api import user_api as user_api
from api.group_api import group_api as group_api
from api.message_api import message_api
from api.event_api import event_api
from model.BaseModel import db
import config
from util.response import response
from util.operate_token import operate_token

app = Flask(__name__)
ctx = app.app_context()
ctx.push()
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
db.init_app(app)
db.create_all()
app.register_blueprint(user_api)
app.register_blueprint(group_api)
app.register_blueprint(message_api)
app.register_blueprint(event_api)


@app.before_request
def before_request():
    if request.path not in config.NOT_CHECK_URL:
        try:
            token_ = request.headers['Authorization']
        except:
            return response(data={'code': 40101}, msg="无访问权限", status=401)
        res = operate_token.validate_token(token_)
        return res
    else:
        # token_ = request.headers['token']
        res = None
    if res:
        return res


@app.after_request
def after_request(res):
    """双重跨域"""
    res.access_control_allow_origin = "*"
    res.access_control_allow_methods = ["GET", "POST", "OPTIONS"]
    res.access_control_allow_headers = "*"
    res.access_control_max_age = "7200"
    res.access_control_allow_credentials = "true"
    if request.method == "OPTIONS":
        res.status = 200
    return res


@app.route('/')
def hello_world():
    return response(msg="重定向到登录页面")


@app.route("/about")
def about():
    return "关于我们"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6543, debug=False, threaded=True)
