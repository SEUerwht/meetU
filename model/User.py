from model.BaseModel import BaseModel,db

class user(BaseModel):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,nullable=False, comment="用户id")
    username = db.Column(db.String(100), nullable=False, comment="用户名", unique=True)
    password = db.Column(db.String(100), nullable=False, comment="密码")
    phone = db.Column(db.String(20), nullable=True, comment="电话号码", unique=True)
    email = db.Column(db.String(30), nullable=True, comment="邮箱", unique=True)
    age = db.Column(db.Integer, nullable=True, comment="年龄")
    gender = db.Column(db.Integer, nullable=True,comment="性别")
