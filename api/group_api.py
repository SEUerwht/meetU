from flask import Blueprint, request, g
from model.Group import Group
from model.User import User
from model.GroupUser import GroupUser
from model.Photo import Photo
from util.response import response, model_to_dict
from model.BaseModel import db
from service.file_deal import upload_file


group_api = Blueprint("group_api", __name__, url_prefix='/group')


@group_api.post("/create")
def create_group():
    '''本接口只对管理员开放，作用是创建群组'''
    group_name = request.json.get("group_name")
    group_type = request.json.get("group_type")
    admin_id = g.user["id"]
    group_information = request.json.get("group_information")
    group_ = Group(group_name=group_name, admin_id=admin_id, group_information=group_information)
    db.session.add(group_)
    db.session.flush()
    group_admin = GroupUser(
        group_id=group_.id, user_id=admin_id, user_allow=1, group_type=group_type
    )
    db.session.add(group_admin)
    db.session.commit()
    return response(msg="创建群组成功")

@group_api.post("/update")
def update_group():
    '''管理员更新群组信息'''
    group_id = request.json.get("id")
    group_name = request.json.get("group_name")
    group_position = request.json.get("group_position")
    group_public = request.json.get("group_public")
    group_information = request.json.get("group_information")
    group_type = request.json.get("group_type")
    user_id = g.user["id"]
    group_ = Group.query.filter(Group.admin_id == user_id).filter(Group.id == group_id).first()
    if not group_:
        return response(msg="您不是管理员，所以没有权限", status=400)
    else:
        group_.group_name = group_name
        group_.group_position = group_position
        group_.group_public = group_public
        group_.group_information = group_information
        group_.group_type = group_type
        db.session.commit()
        return response(msg="修改group信息成功")

@group_api.post("/delete")
def delete_group():
    '''管理员删除群组'''
    group_id = request.json.get("group_id")
    user_id = g.user["id"]
    user_ = Group.query.filter(Group.admin_id == user_id).filter(Group.id == group_id).first()
    if not user_:
        return response(msg="您没有权限或者该群组不存在", status=400)
    else:
        group = Group.query.filter(Group.id == group_id).first()
        group_user = GroupUser.query.filter(GroupUser.group_id == group_id).all()
        db.session.delete(group)
        for group_user_ in group_user:
            db.session.delete(group_user_)
        db.session.commit()
        return response(msg="删除group成功")

@group_api.get("/query")
def query_group():
    '''查询群组信息，该接口对管理员及组员开放'''
    group_id = request.args.get("group_id")
    group = db.session.query(Group, User.username).outerjoin(User, Group.admin_id == User.id).filter(Group.id == group_id).first()
    if not group:
        return response(msg="没有找到对应群组", status=400)
    date = {
        **model_to_dict(group[0]),
        "admin_name": group[1]
    }
    if not group:
        return response(msg="没有查询到相应的群组", status=400)
    return response(data=date, msg="查询单个group信息成功")

@group_api.get("/query_allgroup")
def query_allgroup():
    page = int(request.args.get("page"))
    count = int(request.args.get("count"))
    group_type = request.args.get("group_type")
    kw = request.args.get("kw")
    is_admin = request.args.get("is_admin")
    group_ = db.session.query(Group, User.username).outerjoin(User, Group.admin_id == User.id)
    if group_type:
        group_ = group_.filter(Group.group_type == group_type)
    if kw:
        group_ = group_.filter(Group.group_name.contains(kw))
    if is_admin:
        group_ = group_.filter(Group.admin_id == g.user["id"])
    groups = group_.paginate(page=page, count=count, error_out=False).items
    total = group_.count()
    data_group = []
    for group in groups:
        data_group.append({
            **model_to_dict(group[0]),
            "admin_name": group[1]
        })
    return response(data={
        "groups": data_group,
        "total": total
    }, msg="查找所有群组成功")


@group_api.get("/query_user_group")
def query_user_group():
    page = int(request.args.get("page"))
    count = int(request.args.get("count"))
    group_type = request.args.get("group_type")
    kw = request.args.get("kw")
    group_ = db.session.query(GroupUser, Group).outerjoin(
        Group, Group.id == GroupUser.group_id
    ).filter(
        GroupUser.user_id == g.user["id"],
        GroupUser.user_allow == 1
    )
    if group_type:
        group_ = group_.filter(Group.group_type == group_type)
    if kw:
        group_ = group_.filter(Group.group_name.contains(kw))
    groups = group_.paginate(page=page, count=count, error_out=False).items
    total = group_.count()
    data_group = []
    for group in groups:
        user_ = User.query.filter(User.id == group[1].admin_id).first()
        data_group.append({
            **model_to_dict(group[0]),
            **model_to_dict(group[1]),
            "admin_name": user_.username
        })
    return response(data={
        "groups": data_group,
        "total": total
    }, msg="查找所有群组成功")


@group_api.post("/check_request")
def check_request():
    '''该接口让管理员审核加群申请'''
    group_id = request.json.get("group_id")
    user_id = request.json.get("user_id")
    user_allow = request.json.get("user_allow")
    admin_ = Group.query.filter(Group.id == group_id).first()
    if not admin_ or admin_.admin_id != g.user["id"]:
        return response(msg="没有查询到相应的群组或您没有权限", status=400)
    if user_allow == 0:
        group_user = GroupUser.query.filter(GroupUser.group_id == group_id).filter(GroupUser.user_id == user_id).first()
        group_user.user_allow = 2
        db.session.commit()
        return response(msg="已拒绝该用户加群")
    else:
        group_user = GroupUser.query.filter(GroupUser.group_id == group_id).filter(GroupUser.user_id == user_id).first()
        if not group_user:
            return response(msg="没有找到该用户", status=400)
        group_user.user_allow = 1
        admin_.group_nums += 1
        db.session.commit()
        return response(msg="已同意该用户加群")

@group_api.get("/query_checkuser")
def query_checkuser():
    '''该接口是管理员查看申请加群列表的'''
    group_id = request.args.get("group_id")
    page = int(request.args.get("page"))
    count = int(request.args.get("count"))
    kw = request.args.get("kw")
    group_admin = Group.query.filter(Group.admin_id == g.user["id"]).filter(Group.id == group_id).first()
    if not group_admin:
        return response(msg="您不是管理员，没有相关权限", status=400)
    group_user = db.session.query(GroupUser, User.username).outerjoin(User, GroupUser.user_id == User.id).filter(
        group_id == GroupUser.group_id
    ).filter(
        GroupUser.user_allow == 0
    )
    if kw:
        group_user = group_user.filter(User.username.contains(kw))
    users = group_user.paginate(page=page, count=count, error_out=False).items
    total = group_user.count()
    users_data = []
    for user_ in users:
        users_data.append({
            **model_to_dict(user_[0]),
            "username": user_[1]
        })
    date = {
        "users": users_data,
        "total": total
    }
    return response(data=date, msg="成功返回所有数据")

@group_api.post("/delete_user")
def delete_user():
    '''该接口是管理员踢人的接口'''
    group_id = request.json.get("group_id")
    user_id = request.json.get("user_id")
    admin_ = Group.query.filter(Group.admin_id == g.user["id"]).filter(Group.id == group_id).first()
    if not admin_:
        return response(msg="您不是管理员，没有相关权限", status=400)
    group_user = GroupUser.query.filter(GroupUser.group_id == group_id).filter(GroupUser.user_id == user_id).first()
    db.session.delete(group_user)
    admin_.group_nums -= 1
    db.session.commit()
    return response(msg="已将该用户移出群")

@group_api.get("/query_user")
def query_alluser():
    '''该接口是查看群组成员，管理员和组员都可以使用'''
    group_id = request.args.get("group_id")
    page = int(request.args.get("page"))
    count = int(request.args.get("count"))
    group_ = Group.query.filter(Group.id == group_id).first()
    if not group_:
        return response(msg="该群组不存在")
    group_user = db.session.query(GroupUser, User.username).outerjoin(User, GroupUser.user_id == User.id).filter(GroupUser.group_id == group_id).filter(GroupUser.user_allow == 1)
    date_user = []
    users = group_user.paginate(page=page, count=count, error_out=False).items
    total = group_user.count()
    for i in users:
        temp = {
            **model_to_dict(i[0]),
            "username": i[1]
        }
        date_user.append(temp)
    return response(data={
        "users": date_user,
        "total": total
    }, msg="成功返回所有数据")

@group_api.post("/join_group")
def join_group():
    '''组员加群申请'''
    group_id = request.json.get("group_id")
    group = Group.query.filter(Group.id == group_id).first()
    if not group:
        return response(msg="没有查询到相应的群组", status=400)
    if group.admin_id == g.user["id"]:
        return response(msg="您是该群的管理员", status=400)
    user_id = g.user["id"]
    user_exist = GroupUser.query.filter(GroupUser.group_id == group_id).filter(GroupUser.user_id == g.user["id"]).first()
    if user_exist and user_exist.user_allow == 1:
        return response(msg="已加入该群当中")
    if user_exist and user_exist.user_allow == 0:
        return response(msg="正在等待管理员的审核")
    if user_exist and user_exist.user_allow == 2:
        user_exist.user_allow = 0
        db.session.commit()
        return response(msg="等待管理员审核")
    group_user = GroupUser(group_id=group_id, user_id=user_id)
    db.session.add(group_user)
    db.session.commit()
    return response(msg="等待管理员审核")

@group_api.post("/exit_group")
def exit_group():
    '''组员退出接口'''
    group_id = request.json.get("group_id")
    group = Group.query.filter(Group.id == group_id).first()
    if not group:
        return response(msg="没有查询到相应的群组", status=400)
    group_user = GroupUser.query.filter(GroupUser.group_id == group_id).filter(GroupUser.user_id == g.user["id"]).first()
    db.session.delete(group_user)
    group.group_nums -= 1
    db.session.commit()
    return response(msg="退出群组成功")

@group_api.post("/add_photo")
def add_photo():
    '''上传照片，管理员和用户接口'''
    photo = request.files.get("photo")
    group_id = request.json.get("group_id")
    post_id = request.json.get("post_id")
    photo_url = upload_file(photo)
    photo_ = Photo(group_id=group_id, post_id=post_id, photo_url=photo_url)
    db.session.add(photo_)
    db.session.commit()
    return response(msg="上传照片成功")

@group_api.get("/query_photo")
def query_photo():
    '''查看照片，管理员和群员都可以使用'''
    group_id = request.args.get("group_id")
    post_id = request.args.get("post_id")
    if not post_id:
        photos = Photo.query.filter(Photo.group_id == group_id).all()
        return response(data=photos, msg="已返回所有照片")
    else:
        photos = Photo.query.filter(Photo.group_id == group_id).fliter(Photo.post_id == post_id).all()
        return response(data=photos, msg="已返回制定上传者上传的所有照片")

@group_api.post("/delete_photo")
def delete_photo():
    '''删除照片，只有管理员可以使用'''
    group_id = request.json.get("group_id")
    photo_id = request.json.get("photo_id")
    admin_ = Group.query.filter(Group.id == group_id).filter(Group.id == group_id).first()
    if admin_.admin_id != g.user["id"]:
        return response(msg="您不是管理员，无权进行操作", status=400)
    photo = Photo.query.filter(Photo.id_ == photo_id).first()
    db.session.delete(photo)
    db.session.commit()
    return response(msg="删除成功")