from flask import Blueprint, request, g
from model.User import User
from model.GroupAdmin import GroupAdmin
from model.GroupUser import GroupUser
from util.response import response
from model.BaseModel import db


group_api = Blueprint("group_api", __name__, url_prefix='/group')


@group_api.post("/create")
def create_group():
    group_name = request.json.get("group_name")
    admin_id = g.user["id"]
    user1 = User.query.filter(User.id == admin_id).first()
    admin_name = user1.username
    message = request.json.get("message")
    group_admin = GroupAdmin(group_name=group_name, admin_id=admin_id, admin_name=admin_name, message=message)
    db.session.add(group_admin)
    db.session.commit()
    return response(msg="创建群组成功")

@group_api.post("/update")
def update_group():
    group_name = request.json.get("group_name")
    message = request.json.get("message")
    user_id = g.user["id"]
    user_ = GroupAdmin.query.filter(GroupAdmin.admin_id == user_id).first()
    if not user_:
        return response(msg="您不是管理员，所以没有权限")
    else:
        user_.group_name = group_name
        user_.message = message
        db.session.commit()
        return response(msg="修改group信息成功")

@group_api.post("/delete")
def delete_group():
    group_id = request.json.get("group_id")
    user_id = g.user["id"]
    user_ = GroupAdmin.query.filter(GroupAdmin.admin_id == user_id).filter(GroupAdmin.group_id == group_id).first()
    if not user_:
        return response(msg="您没有权限或者该群组不存在")
    else:
        group = GroupAdmin.query.filter(GroupAdmin.group_id == group_id).first()
        group_user = GroupUser.query.filter(GroupUser.group_id == group_id).all()
        db.session.delete(group)
        for group_user_ in group_user:
            db.session.delete(group_user_)
        db.session.commit()
        return response(msg="删除group成功")

@group_api.get("/query")
def query_group():
    group_id = request.json.get("group_id")
    group_name = request.json.get("group_name")
    group = GroupAdmin.query.filter(GroupAdmin.group_id == group_id).first()
    if not group:
        return response(msg="没有查询到相应的群组")
    return response(data=group, msg="查询单个group信息成功")

@group_api.post("/check_request")
def check_request():
    group_id = request.json.get("group_id")
    user_id = request.json.get("user_id")
    user_allow = request.json.get("user_allow")
    admin_ = GroupAdmin.query.filter(GroupAdmin.group_id == group_id).first()
    if not admin_ or admin_.admin_id != g.user["id"]:
        return response(msg="没有查询到相应的群组或您没有权限")
    if user_allow == 0:
        group_user = GroupUser.query.filter(GroupUser.group_id == group_id).filter(GroupUser.user_id == user_id).first()
        db.session.delete(group_user)
        db.session.commit()
        return response(msg="已拒绝该用户加群")
    else:
        group_user = GroupUser.query.filter(GroupUser.group_id == group_id).filter(GroupUser.user_id == user_id).first()
        if not group_user:
            return response(msg="没有找到该用户")
        group_user.user_allow = user_allow
        db.session.commit()
        return response(msg="已同意该用户加群")

@group_api.post("/delete_user")
def delete_user():
    group_id = request.json.get("group_id")
    user_id = request.json.get("user_id")
    group_user = GroupUser.query.filter(GroupUser.group_id == group_id).filter(GroupUser.user_id == user_id).first()
    db.session.delete(group_user)
    db.session.commit()
    return response(msg="已将该用户移出群")

@group_api.get("/query_checkuser")
def query_checkuser():
    group_id = request.json.get("group_id")
    group_admin = GroupAdmin.query.filter(GroupAdmin.admin_id == g.user["id"]).first()
    if not group_admin:
        return response(msg="您不是管理员，没有相关权限")
    group_user = GroupUser.query.filter(GroupUser.group_id == group_id).filter(GroupUser.user_allow == 0).all()
    return response(data=group_user, msg="成功返回所有数据")

@group_api.get("/query_user")
def query_alluser():
    list_group_user = []
    group_id = request.json.get("group_id")
    group_ = GroupAdmin.query.filter(GroupAdmin.group_id == group_id).first()
    if not group_:
        return response(msg="该群组不存在")
    group_user = GroupUser.query.filter(GroupUser.group_id == group_id).filter(GroupUser.user_allow == 1).all()
    for user_ in group_user:
        list_group_user.append(user_)
    group_admin = GroupAdmin.query.filter(GroupAdmin.group_id == group_id).all()
    for user_ in group_admin:
        list_group_user.append(user_)
    return response(data=list_group_user, msg="成功返回所有数据")

@group_api.post("/join_group")
def join_group():
    group_id = request.json.get("group_id")
    group = GroupAdmin.query.filter(GroupAdmin.group_id == group_id).first()
    if not group:
        return response(msg="没有查询到相应的群组")
    if group.admin_id == g.user["id"]:
        return response("您是该群的管理员")
    user_id = g.user["id"]
    user_ = User.query.filter(User.id == user_id).first()
    user_name = user_.username
    user_exist = GroupUser.query.filter(GroupUser.group_id == group_id).filter(GroupUser.user_id == g.user["id"]).first()
    if user_exist and user_exist.user_allow == 1:
        return response(msg="已加入该群当中")
    if user_exist and user_exist.user_allow == 0:
        return response(msg="正在等待管理员的审核")
    group_user = GroupUser(group_id = group_id, user_id=user_id, user_name=user_name)
    db.session.add(group_user)
    db.session.commit()
    return response(msg="等待管理员审核")

@group_api.post("/exit_group")
def exit_group():
    group_id = request.json.get("group_id")
    group = GroupUser.query.filter(GroupUser.group_id == group_id).first()
    if not group:
        return response(msg="没有查询到相应的群组")
    group_user = GroupUser.query.filter(GroupUser.group_id == group_id).filter(GroupUser.user_id == g.user["id"]).first()
    # print(group_user)
    db.session.delete(group_user)
    db.session.commit()
    return response(msg="退出群组成功")
