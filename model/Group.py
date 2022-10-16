from model.BaseModel import BaseModel, db


class Group(BaseModel):
    __tablename__ = "group"
    id = db.Column(db.Integer, primary_key=True, comment="群组id")
    group_name = db.Column(db.String(30), index=True, nullable=False, comment="群组名称")
    admin_id = db.Column(db.Integer, index=True, nullable=False, comment="群组管理员")
    group_position = db.Column(db.String(20), index=True, nullable=True, comment="群组位置")
    group_public = db.Column(db.Integer, nullable=False, default=1, comment="群组是否公开")
    group_nums = db.Column(db.Integer, nullable=False, default=1, comment="群组人数")
    group_information = db.Column(db.String(1024), nullable=True, comment="群简介")
    group_type = db.Column(db.Integer, nullable=True, index=True, comment="群组类型")