from model.BaseModel import db,BaseModel

class Photo(BaseModel):
    __tablename__ = "photo"
    id = db.Column(db.Integer, primary_key=True, comment="id")
    group_id = db.Column(db.Integer, index=True, nullable=False, comment="group_id")
    post_id = db.Column(db.Integer, index=True, nullable=False, comment="上传图片组员id")
    photo_url = db.Column(db.String(30), index=True, nullable=False, comment="图片的url")