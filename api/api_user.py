from flask import Blueprint,request
from model.User import user
from util.Response import response
from util.operate_token import operate_token
import util.config as config
from util.redis import redis_db
from model.BaseModel import db

bp = Blueprint("api_user",__name__,url_prefix='/user')

@bp.post("/login")
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    # password = "123456"
    token = None
    user1 = user.query.filter(user.username==username).first()
    if not user1:
        return response(data={"code": 40101}, msg="该用户不存在,请创建用户", status=401)

    elif(user1.password == password):
        token = operate_token.create_token(username)
        redis_db.set(token,token,config.EXPIRE_TIME)
        return token
    else:
        return response(data={"code": 40101}, msg="密码错误", status=401)

@bp.post("/register")
def register():
    username = request.json.get("username")
    password = request.json.get("password")
    phone = request.json.get("phone")
    email = request.json.get("email")
    age = request.json.get("age")
    user_ = user(username=username, password=password, phone=phone, email=email, age=age)
    db.session.add(user_)
    db.session.commit()
    return response(data={"code": 40101}, msg="注册成功", status=200)

