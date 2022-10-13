from flask import Flask,redirect,request
from api.api_user import user_bp as user_bp
from model.BaseModel import db
import util.config as config
from util.Response import response
from util.operate_token import operate_token

app = Flask(__name__)
ctx = app.app_context()
ctx.push()
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
db.init_app(app)
db.create_all()
app.register_blueprint(user_bp)


@app.before_request
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

@app.route('/')
def hello_world():
    return redirect("/user/login")

@app.route("/about")
def about():
    return "关于我们"


if __name__ == '__main__':
    app.run(port=7070)
