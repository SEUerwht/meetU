from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False, comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False, comment="更新时间")