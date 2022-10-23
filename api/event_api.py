from flask import Blueprint, request, g
from model.Group import Group
from model.User import User
from model.Event import Event
from model.EventUser import EventUser
from model.GroupUser import GroupUser
from util.response import response, model_to_dict
from model.BaseModel import db


event_api = Blueprint("event_api", __name__, url_prefix='/event')


@event_api.post("/create_event")
def create_event():
    '''创建一个活动'''
    event_name = request.json.get("event_name")
    event_information = request.json.get("event_information")
    admin_id = g.user["id"]
    group_id = request.json.get("group_id")
    event_type = request.json.get("event_type")
    event_img = request.json.get("event_img")
    # 判断创建人是否是该群里面的人员
    admin = Group.query.filter(Group.id == group_id).filter(Group.admin_id == g.user["id"]).first()
    if not admin:
        user = GroupUser.query.filter(GroupUser.group_id == group_id).filter(GroupUser.user_id == g.user["id"]).filter(GroupUser.user_allow == 1).first()
        if not user:
            return response(msg="您不是群组人员，无法创立活动", status=400)
    event = Event(
        event_name=event_name,
        event_information=event_information,
        admin_id=admin_id,
        group_id=group_id,
        event_type=event_type,
        event_img=event_img
    )
    db.session.add(event)
    db.session.commit()
    return response(msg="创建活动成功")

@event_api.post("/update_event")
def update_event():
    '''更新活动信息'''
    event_id = request.json.get("id")
    event_name = request.json.get("event_name")
    event_type = request.json.get("event_type")
    event_information = request.json.get("event_information")
    event_status = request.json.get("event_status")
    event = Event.query.filter(Event.id == event_id).first()
    if not event:
        return response(msg="没有找到相应的活动", status=400)
    if event.admin_id != g.user["id"]:
        group_admin = Group.query.filter(Group.admin_id == g.user["id"]).filter(Group.id == event.group_id).first()
        if not group_admin:
            return response(msg="您没有权限", status=400)
    event.event_name = event_name
    event.event_type = event_type
    event.event_status = event_status
    event.event_information = event_information
    db.session.commit()
    return response(msg="修改活动信息成功")

@event_api.post("/delete_event")
def delete_event():
    '''删除活动'''
    event_id = request.json.get("event_id")
    event = Event.query.filter(Event.id == event_id).first()
    if not event:
        return response(msg="没有找到相应的活动", status=400)
    if event.admin_id != g.user["id"]:
        group_admin = Group.query.filter(Group.admin_id == g.user["id"]).filter(Group.id == event.group_id).first()
        if not group_admin:
            return response(msg="您没有权限", status=400)
    db.session.delete(event)
    users = EventUser.query.filter(EventUser.event_id == event_id).all()
    for user in users:
        db.session.delete(user)
    db.session.commit()
    return response(msg="删除活动成功")

@event_api.get("/query_event")
def query_event():
    '''查找活动，可以是所有活动，管理员查看自己所管理的活动也是这个接口'''
    event_id = request.args.get("event_id")
    event = db.session.query(Event, User.username).outerjoin(
        User, Event.admin_id == User.id
    ).filter(Event.id == event_id).first()
    if not event:
        return response(msg="活动不存在", status=400)
    group = Group.query.filter(
        Group.id == event[0].group_id
    ).first()
    event_info = {
        **model_to_dict(event[0]),
        "admin_name": event[1],
        "group_name": group.group_name
    }
    return response(data=event_info, msg="成功返回数据")

@event_api.get("/query_events")
def query_events():
    '''查找活动，可以是所有活动，管理员查看自己所管理的活动也是这个接口'''
    group_id = request.args.get("group_id")
    event_type = request.args.get("event_type")
    event_status = request.args.get("event_status")
    admin_id = request.args.get("admin_id")
    page = int(request.args.get("page"))
    count = int(request.args.get("count"))
    kw = request.args.get("kw")
    events = db.session.query(Event, User.username).outerjoin(User, Event.admin_id == User.id)
    if group_id:
        events = events.filter(Event.group_id == group_id)
    if kw:
        events = events.filter(Event.event_name.contains(kw))
    if event_type:
        events = events.filter(Event.event_type == event_type)
    if event_status:
        events = events.filter(Event.event_status == event_status)
    if admin_id:
        events = events.filter(Event.admin_id == admin_id)
    event = events.paginate(page=page, count=count, error_out=False).items
    total = events.count()
    events_info = []
    for i in event:
        events_info.append({
            **model_to_dict(i[0]),
            "admin_name": i[1]
        })
    return response(data={
        "events": events_info,
        "count": total
    }, msg="成功返回数据")


@event_api.get("/query_alluser")
def query_alluser():
    '''查看活动中的所有成员'''
    event_id = request.args.get("event_id")
    page = int(request.args.get("page"))
    count = int(request.args.get("count"))
    kw = request.args.get("kw")
    event = Event.query.filter(Event.id == event_id).first()
    if not event:
        return response(msg="该活动不存在", status=400)
    admin_exist = EventUser.query.filter(EventUser.user_id == event.admin_id).filter(EventUser.event_id == event_id).first()
    if not admin_exist:
        user = EventUser(event_id=event_id, user_id=event.admin_id)
        db.session.add(user)
        db.session.commit()
    event_users = db.session.query(EventUser, User.username).outerjoin(User, EventUser.user_id == User.id).filter(
        EventUser.event_id == event_id)
    if kw:
        event_users = event_users.filter(User.username.contains(kw))
    users = event_users.paginate(page=page, count=count, error_out=False).items
    total = event_users.count()
    users_info = []
    for user in users:
        users_info.append({
            **model_to_dict(user[0]),
            "user_name": user[1]
        })
    return response(data={
        "users": users_info,
        "total": total
    }, msg="返回成员数据成功")


@event_api.post("/join_event")
def join_event():
    '''加入活动'''
    print(request.json)
    event_id = request.json.get("event_id")
    group_id = request.json.get("group_id")
    admin = Event.query.filter(Event.id == event_id).filter(Event.admin_id == g.user["id"]).first()
    if admin:
        return response(msg="您是该活动的管理员，不需要加入了", status=400)
    user = EventUser.query.filter(Event.id == event_id).filter(EventUser.user_id == g.user["id"]).first()
    if user:
        return response(msg="您已加入了该活动", status=400)
    group_user = GroupUser.query.filter(GroupUser.group_id == group_id).filter(GroupUser.user_id == g.user["id"]).first()
    if not group_user:
        return response(msg="您不是该群组成员，请先加群", status=400)
    new_user = EventUser(event_id=event_id, user_id=g.user["id"])
    db.session.add(new_user)
    event = Event.query.filter(Event.id == event_id).first()
    event.event_nums += 1
    db.session.commit()
    return response(msg="您成功加入该活动")

@event_api.post("/exit_event")
def exit_event():
    '''退出活动'''
    event_id = request.json.get("event_id")
    event = Event.query.filter(Event.id == event_id).first()
    if not event:
        return response(msg="该活动不存在", status=400)
    admin = Event.query.filter(Event.id == event_id).filter(Event.admin_id == g.user["id"]).first()
    if admin:
        return response(msg="您是管理员不能退出活动，或者您可以选择解散该活动", status=400)
    user = EventUser.query.filter(EventUser.event_id == event_id).filter(EventUser.user_id == g.user["id"]).first()
    db.session.delete(user)
    event.event_nums -= 1
    db.session.commit()
    return response(msg="退出活动成功")

@event_api.get("/query_join_event")
def query_join_event():
    '''查看加入的活动'''
    event_type = request.args.get("event_type")
    admin_id = request.args.get("admin_id")
    page = int(request.args.get("page"))
    count = int(request.args.get("count"))
    kw = request.args.get("kw")
    events = db.session.query(Event).outerjoin(EventUser, Event.id == EventUser.event_id).filter(EventUser.user_id == g.user["id"])
    if kw:
        events = events.filter(Event.event_name.contains(kw))
    if event_type:
        events = events.filter(Event.event_type == event_type)
    if admin_id:
        events = events.filter(Event.admin_id == admin_id)
    event = events.paginate(page=page, count=count, error_out=False).items
    total = events.count()
    return response(data={
        "events": model_to_dict(event),
        "count": total
    }, msg="成功返回数据")

@event_api.post("/delete_user")
def delete_user():
    '''管理员删除活动的成员'''
    event_id = request.json.get("event_id")
    user_id = request.json.get("user_id")
    admin = Event.query.filter(Event.admin_id == g.user["id"]).first()
    if not admin:
        return response(msg="您没有权限", status=400)
    user = EventUser.query.filter(EventUser.event_id == event_id).filter(EventUser.user_id == user_id).first()
    db.session.delete(user)
    db.session.commit()
    return response(msg="删除活动成员成功")