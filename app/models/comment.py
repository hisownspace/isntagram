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
    """Comment model for alembic and SQLAlchemy
    
    has many-to-many relationship with users on liked_comment table (above)
    """
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False,)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=False)
    content = db.Column(db.String(2200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

    user = db.relationship('User', back_populates='comments')
    image = db.relationship('Image', back_populates='comments')

    user_likes = db.relationship('User',
                                secondary=liked_comment,
                                back_populates='liked_comments')

    def to_dict(self):
        """Returns a dictionary representing comment object for use in http responses"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "image_id": self.image_id,
            "content": self.content,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "user": (self.user.id, self.user.username),
            "user_likes": [(user.id, user.username) for user in self.user_likes],
            "num_likes": len(self.user_likes),
        }