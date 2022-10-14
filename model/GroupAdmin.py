from model.BaseModel import BaseModel, db


class GroupAdmin(BaseModel):
    __tablename__ = "group_admin"
    group_id = db.Column(db.Integer, primary_key=True, comment="群组id")
    group_name = db.Column(db.String(30), nullable=False, comment="群组名称")
    admin_id = db.Column(db.Integer, index=True, nullable=False, comment="群组管理员")
    admin_name = db.Column(db.String(20), nullable=False, comment="管理员用户名")
    message = db.Column(db.String(1024), nullable=True, comment="群组消息（暂时用于测试）")