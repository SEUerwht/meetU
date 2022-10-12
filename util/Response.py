from flask import make_response, jsonify
from model.BaseModel import BaseModel
from datetime import datetime


def model_to_dict(model):
    """模型转字典"""
    if type(model) is list:
        return [model_to_dict(e) for e in model]
    if not model:
        return None

    d = {}
    for c in model.__table__.columns:
        attr = getattr(model, c.name)
        if isinstance(attr, datetime):
            # 格式化时间字段
            attr = attr.strftime("%Y-%m-%d %H:%M:%S")
        d[c.name] = attr
    return d


def response(data=None, msg="success", status=200):
    """封装响应"""
    if isinstance(data, BaseModel):
        # data为单个对象
        data = model_to_dict(data)
    elif type(data) is list:
        if not data:
            data = []
        elif isinstance(data[0], BaseModel):
            # data为对象列表
            data = [model_to_dict(e) for e in data]
    body = jsonify(data=data, msg=msg)
    response_ = make_response(body, status)
    return response_