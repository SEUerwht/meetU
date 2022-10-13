from model.BaseModel import BaseModel, db


class Message(BaseModel):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True, nullable=False, comment="消息id")
    s_id = db.Column(db.Integer, nullable=False, index=True, comment="发送人id")
    to_id = db.Column(db.Integer, nullable=False, index=True, comment="接收人id")
    content = db.Column(db.String(1024), nullable=False, comment="消息内容")
    is_read = db.Column(db.Integer, nullable=False, default=0, comment="是否已读")
