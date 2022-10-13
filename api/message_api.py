from flask import Blueprint, request, redirect, g
from model.Message import Message
from util.response import response
from util.response import model_to_dict
from model.BaseModel import db
from sqlalchemy import and_, not_, or_

message_api = Blueprint("message_api", __name__, url_prefix='/message')


@message_api.post('/send_message')  # route任何请求类型都可以
def send_message():
    # s_id = request.json.get("s_id")
    s_id = g.user["id"]  # g的作用是此次请求的全局变量
    to_id = request.json.get("to_id")
    if s_id == to_id:
        return response(msg="发送人不能与接收人一致", status=401)
    content = request.json.get("content")
    title = request.json.get("title")
    message_ = Message(s_id=s_id, to_id=to_id, title=title, content=content)
    db.session.add(message_)
    db.session.commit()   # 增，删，改操作之后都要commit
    return response(msg="发送成功")


@message_api.get('/get_sender_message')
def get_sender_message():
    # s_id = request.args.get("s_id")  # args是url后 ?s_id=xx,get的body直接写在url后
    s_id = g.user["id"]
    page = int(request.args["page"])  # 等价于page = int(request.args.get("page")),但get可以返回NULL,所以必备字段用中括号
    count = int(request.args["count"])
    kw = request.args.get("kw")  # 模糊查询

    q = Message.query.filter(Message.s_id == s_id)  # .all()查询所有
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

    q = Message.query.filter(Message.to_id == to_id)  # .all()查询所有
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
