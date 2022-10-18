from model.BaseModel import BaseModel, db


class Message(BaseModel):
    __tablename__ = "message"  # __xx__ mean?
    id = db.Column(db.Integer, primary_key=True, nullable=False, comment="消息id")
    title = db.Column(db.String(1024), nullable=False, comment="消息题目")
    content = db.Column(db.String(1024), nullable=False, comment="消息内容")
    s_id = db.Column(db.Integer, nullable=False, index=True, comment="发送人id")


class MessageUser(BaseModel):
    __tablename__ = "message_user"
    id = db.Column(db.Integer, primary_key=True, nullable=False, comment="消息发送记录id")
    to_id = db.Column(db.Integer, nullable=False, index=True, comment="接收人id")
    message_id = db.Column(db.Integer, nullable=False, index=True, comment="消息id")
    is_read = db.Column(db.Integer, nullable=False, default=0, comment="是否已读")