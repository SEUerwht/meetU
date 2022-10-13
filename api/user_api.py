from flask import Blueprint, request, redirect
from model.User import User
from util.response import response
from util.operate_token import operate_token
import config as config
from util.redis_util import redis_db
from model.BaseModel import db

user_api = Blueprint("user_api", __name__, url_prefix='/user')


@user_api.post("/login")
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    user1 = User.query.filter(User.username == username).first()
    if not user1:
        return response(data={"code": 40101}, msg="该用户不存在,请创建用户", status=401)
    elif user1.password == password:
        token = operate_token.create_token(username)
        redis_db.set(token, token, config.EXPIRE_TIME)
        return token
    else:
        return response(data={"code": 40101}, msg="密码错误", status=401)


@user_api.post("/register")
def register():
    username = request.json.get("username")
    password = request.json.get("password")
    user_ = User(username=username, password=password)
    db.session.add(user_)
    db.session.commit()
    return response(data={"code": 40101}, msg="注册成功", status=200)


@user_api.post("/logout")
def layout():
    token_ = request.headers.get('token')
    redis_db.delete(token_)
    return redirect("/")
