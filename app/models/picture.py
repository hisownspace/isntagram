from datetime import datetime
from .db import db
from .tag import tagged_picture

liked_picture = db.Table('liked_picture',
    db.Column('user_id',
                db.Integer,
                db.ForeignKey("users.id"),
                nullable=False),
    db.Column('picture_id',
                db.Integer,
                db.ForeignKey("pictures.id"),
                nullable=False)
)

class Picture(db.Model):
    __tablename__ = "pictures"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False, unique=True)
    caption = db.Column(db.String(2200), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    user = db.relationship('User', back_populates='pictures')
    comments = db.relationship('Comment', back_populates='picture')

    tags = db.relationship('Tag',
                            secondary=tagged_picture,
                            back_populates="pictures")
                            
    user_like = db.relationship('User',
                                secondary=liked_picture,
                                back_populates='liked_picture')

