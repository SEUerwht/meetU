from model.BaseModel import BaseModel, db


class GroupUser(BaseModel):
    __tablename__ = "group_user"
    id = db.Column(db.Integer, primary_key=True, comment="id")
    group_id = db.Column(db.Integer, index=True, nullable=False, comment="群组id")
    user_id = db.Column(db.Integer, index=True, nullable=False, comment="群组成员id")
    user_allow = db.Column(db.Integer, default=0, nullable=False, comment="是否通过管理员同意加群")