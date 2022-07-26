from datetime import datetime
from .db import db
from .tag import tagged_image

liked_image = db.Table('liked_image',
    db.Column('user_id',
                db.Integer,
                db.ForeignKey("users.id"),
                nullable=False),
    db.Column('image_id',
                db.Integer,
                db.ForeignKey("images.id"),
                nullable=False)
)

class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False, unique=True)
    caption = db.Column(db.String(2200), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

    user = db.relationship('User', back_populates='images')
    comments = db.relationship('Comment', back_populates='image')

    tags = db.relationship('Tag',
                            secondary=tagged_image,
                            back_populates="images")
                            
    user_likes = db.relationship('User',
                                secondary=liked_image,
                                back_populates='liked_images')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "url": self.url,
            "caption": self.caption,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "comments": [comment.to_dict() for comment in self.comments],
            "tags": [tag.to_dict() for tag in self.tags],
            "user_likes": [(user.id, user.username) for user in self.user_likes],
            "num_likes": len(self.user_likes)
        }