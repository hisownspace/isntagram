from datetime import datetime
from .db import db


liked_comment = db.Table('liked_comment',
    db.Column('user_id',
                db.Integer,
                db.ForeignKey("users.id"),
                nullable=False),
    db.Column('comment_id',
                db.Integer,
                db.ForeignKey("comments.id"),
                nullable=False)
)

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False,)
    picture_id = db.Column(db.Integer, db.ForeignKey('pictures.id'), nullable=False)
    content = db.Column(db.String(2200), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    user = db.relationship('User', back_populates='comments')
    picture = db.relationship('Image', back_populates='comments')

    user_like = db.relationship('User',
                                secondary=liked_comment,
                                back_populates='liked_comment')
