from flask import Blueprint, request, redirect, g
from model.Message import Message
from model.Message import MessageUser
from model.User import User
from util.response import response
from util.response import model_to_dict
from model.BaseModel import db

message_api = Blueprint("message_api", __name__, url_prefix='/message')


@message_api.post('/send_message')  # route任何请求类型都可以
def send_message():
    # s_id = request.json.get("s_id")
    s_id = g.user["id"]  # g的作用是此次请求的全局变量
    to_ids = request.json.get("to_ids")
    if len(to_ids) == 1 and to_ids[0] == g.user["id"]:
        return response(msg="消息不能发送给本人")
    content = request.json.get("content")
    title = request.json.get("title")
    message_ = Message(s_id=s_id, title=title, content=content)
    db.session.add(message_)
    db.session.flush()  # 模拟提交到数据库
    for to_id in to_ids:
        if to_id != g.user["id"]:
            message_user = MessageUser(to_id=to_id, message_id=message_.id)
            db.session.add(message_user)
    db.session.commit()   # 增，删，改操作之后都要commit
    return response(msg="发送成功")


@message_api.get('/get_sender_message')
def get_sender_message():
    # s_id = request.args.get("s_id")  # args是url后 ?s_id=xx,get的body直接写在url后
    s_id = g.user["id"]
    page = int(request.args["page"])  # 等价于page = int(request.args.get("page")),但get可以返回NULL,所以必备字段用中括号
    count = int(request.args["count"])
    kw = request.args.get("kw")  # 模糊查询
    q = Message.query.filter(Message.s_id == s_id)
    print(q)
    if kw:
        q = q.filter(
            Message.title.contains(kw)
        )
    messages = q.paginate(page=page, per_page=count, error_out=False).items
    total = q.count()
    data = {
        "messages": model_to_dict(messages),
        "total": total
    }
    return response(data=data, msg="查询成功")


@message_api.get('/get_receiver_message')
def get_receiver_message():
    to_id = g.user["id"]
    page = int(request.args["page"])  # 等价于page = int(request.args.get("page")),但get可以返回NULL,所以必备字段用中括号
    count = int(request.args["count"])
    kw = request.args.get("kw")  # 模糊查询
    q = db.session.query(MessageUser, Message).outerjoin(
        Message, MessageUser.message_id == Message.id
    ).filter(
        MessageUser.to_id == to_id
    )
    if kw:
        q = q.filter(
            Message.title.contains(kw)
        )
    messages = q.paginate(page=page, per_page=count, error_out=False).items
    messages = [
        {
            **model_to_dict(e[0]),
            **model_to_dict(e[1])
        } for e in messages
    ]
    total = q.count()
    data = {
        "messages": messages,
        "total": total
    }
    return response(data=data, msg="查询成功")


@message_api.get('/get_message_detail')
def get_message_detail():
    message_id = int(request.args["message_id"])
    q = MessageUser.query.filter(MessageUser.message_id == message_id).all()
    print(q)
    users = []
    for e in q:
        users.append(e.to_id)
    print(users)
    q = User.query.filter(User.id.in_(users))
    detail = q.all()
    print(detail)
    total = q.count()
    print(total)
    data = {
        "users": model_to_dict(detail),
        "total": total
    }
    return response(data=data, msg="查询成功")
