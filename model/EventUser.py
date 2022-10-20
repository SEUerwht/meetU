from model.BaseModel import BaseModel, db


class EventUser(BaseModel):
    __tablename__ = "event_user"
    id = db.Column(db.Integer, primary_key=True, comment="id")
    event_id = db.Column(db.Integer, index=True, nullable=False, comment="活动id")
    user_id = db.Column(db.Integer, index=True, nullable=False, comment="活动成员id")