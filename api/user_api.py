from flask import Blueprint, request, redirect, g
from model.User import User
from util.response import response
from util.operate_token import operate_token
import config as config
from util.redis_util import redis_db
from model.BaseModel import db
import service.file_deal as file_deal


user_api = Blueprint("user_api", __name__, url_prefix='/user')


@user_api.post("/login")
def login():
    # id = request.json.get("user_id")
    username = request.json.get("username")
    password = request.json.get("password")
    user1 = User.query.filter(User.username == username).first()
    if not user1:
        return response(msg="该用户不存在,请创建用户", status=401)
    elif user1.password == password:
        token = operate_token.create_token(user1.id)
        redis_db.set(token, token, config.EXPIRE_TIME)
        return token
    else:
        return response(msg="密码错误", status=401)


@user_api.post("/register")
def register():
    username = request.json.get("username")
    password = request.json.get("password")
    user_temp = User.query.filter(User.username == username).first()
    if user_temp:
        return response(msg="用户已存在")
    user_ = User(username=username, password=password)
    db.session.add(user_)
    db.session.commit()
    return response(msg="注册成功")


@user_api.post("/logout")
def layout():
    token_ = request.headers.get('token')
    redis_db.delete(token_)
    return redirect("/user/login")

@user_api.post("update")
def update():
    username = request.json.get("username")
    password = request.json.get("password")
    gender = request.json.get("gender")
    phone = request.json.get("phone")
    interest = request.json.get("interest")
    profit = request.json.get("profit")
    socail_media = request.json.get("social_media")
    email = request.json.get("email")
    icon = request.files.get("icon")
    file_url = file_deal.upload_file(icon)
    file_deal.delete(file_url)
    user_ = User.query.filter(User.id == g.user["id"]).first()
    # 判断是否是别人的名字
    user1 = User.query.filter(User.username == username).first()
    if user1 and user1.id != g.user["id"]:
        return response(msg="当前用户名已存在", status=401)
    user2 = User.query.filter(User.id == user_.email).first()
    if user2 and user2.id != g.user["id"]:
        return response(msg="当前邮箱已存在", status=401)
    user3 = User.query.filter(User.id == user_.phone).first()
    if user3 and user3.id != g.user["id"]:
        return response(msg="当前手机号已存在", status=401)
    if user_:
        user_.username = username
        user_.password = password
        user_.gender = gender
        user_.phone = phone
        user_.email = email
        user_.interest = interest
        user_.profit = profit
        user_.social = socail_media
        user_.icon = file_url
        db.session.commit()
    user_ = User.query.filter(User.id == g.user["id"]).first()
    return response(data=user_, msg="成功修改数据")


@user_api.get("/get_user")
def get_user():
    user_ = User.query.filter(User.id == g.user["id"]).first()
    return response(data=user_, msg="成功返回用户数据")


@user_api.get("/help")
def get_help():
    return response(data={"url": config.HELP_PATH}, msg="成功获得帮助文档")





