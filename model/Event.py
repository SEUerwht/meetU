from model.BaseModel import BaseModel, db


class Event(BaseModel):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True, comment="活动id")
    event_name = db.Column(db.String(30), index=True, nullable=False, comment="活动名称")
    admin_id = db.Column(db.Integer, index=True, nullable=False, comment="活动管理员")
    group_id = db.Column(db.Integer, index=True, nullable=False, comment="隶属于群组的id")
    event_nums = db.Column(db.Integer, nullable=False, default=1, comment="参加活动人数")
    event_information = db.Column(db.String(1024), nullable=True, comment="活动简介")
    event_type = db.Column(db.Integer, nullable=True, index=True, comment="活动类型")
    event_status = db.Column(db.Integer, nullable=False, default=1, index=True, comment="活动状态")
    event_img = db.Column(db.String(255), nullable=True, comment="活动封面")
