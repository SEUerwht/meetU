from flask import Blueprint, request, redirect, g
from model.User import User
from util.response import response, model_to_dict
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
        user_info = model_to_dict(user1)
        del user_info["password"]
        data = {
            "token": token,
            "user_info": user_info
        }
        # data = {
        #     "token": token,
        #     "user_id": id,
        #     "username": user1.username,
        #     "phone": user1.phone,
        #     "email": user1.email,
        #     "age": user1.age,
        #     "gender": user1.gender,
        #     "profit": user1.profit,
        #     "interest": user1.interest,
        #     "social_media": user1.social_media,
        #     "icon": user1.icon
        # }
        return response(data=data, msg="登录成功")
    else:
        return response(msg="密码错误", status=400)


@user_api.post("/register")
def register():
    username = request.json.get("username")
    password = request.json.get("password")
    user_temp = User.query.filter(User.username == username).first()
    if user_temp:
        return response(msg="用户已存在", status=400)
    user_ = User(username=username, password=password)
    db.session.add(user_)
    db.session.commit()
    return response(msg="注册成功")


@user_api.get("/logout")
def layout():
    token_ = request.headers.get('token')
    redis_db.delete(token_)
    return response(msg="退出成功")

@user_api.post("update")
def update():
    username = request.json.get("username")
    password = request.json.get("password")
    age = request.json.get("age")
    gender = request.json.get("gender")
    phone = request.json.get("phone")
    interest = request.json.get("interest")
    profit = request.json.get("profit")
    social_media = request.json.get("social_media")
    email = request.json.get("email")
    icon = request.json.get("icon")
    user_ = User.query.filter(User.id == g.user["id"]).first()
    if icon != user_.icon:
        file_deal.delete(user_.icon)
    # 判断是否是别人的名字
    user1 = User.query.filter(User.username == username).first()
    if user1 and user1.id != g.user["id"]:
        return response(msg="当前用户名已存在", status=400)
    user2 = User.query.filter(User.id == user_.email).first()
    if user2 and user2.id != g.user["id"]:
        return response(msg="当前邮箱已存在", status=400)
    user3 = User.query.filter(User.id == user_.phone).first()
    if user3 and user3.id != g.user["id"]:
        return response(msg="当前手机号已存在", status=400)
    if user_:
        user_.username = username
        user_.password = password
        user_.age = age
        user_.gender = gender
        user_.phone = phone
        user_.email = email
        user_.interest = interest
        user_.profit = profit
        user_.social_media = social_media
        user_.icon = icon
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


@user_api.post("/upload_file")
def upload_file():
    file = request.files.get("file")
    file_url = None
    if file:
        file_url = file_deal.upload_file(file)
    return response(data={"file_url": file_url})
