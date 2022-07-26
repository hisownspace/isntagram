from .db import db
from .comment import liked_comment
from .image import liked_image
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Self-referential join table to track followers and followees
follows = db.Table('follows',
    db.Column('follower_id',
                db.Integer,
                db.ForeignKey("users.id"),
                nullable=False),
    db.Column('followed_id',
                db.Integer,
                db.ForeignKey('users.id'),
                nullable=False)
)

requests = db.Table('follow_requests',
    db.Column('requester_id',
                db.Integer,
                db.ForeignKey("users.id"),
                nullable=False),
    db.Column('requested_id',
                db.Integer,
                db.ForeignKey("users.id"),
                nullable=False)
)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    full_name = db.Column(db.String(40), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

    comments = db.relationship('Comment', back_populates='user')
    images = db.relationship('Image', back_populates='user')

    liked_comments = db.relationship('Comment',
                                    secondary=liked_comment,
                                    back_populates='user_likes')
    
    liked_images = db.relationship('Image',
                                    secondary=liked_image,
                                    back_populates='user_likes')
    
    following = db.relationship('User',
                                secondary=follows,
                                primaryjoin=(follows.c.follower_id == id),
                                secondaryjoin=(follows.c.followed_id == id),
                                backref=db.backref('followers', lazy='dynamic'),
                                )

    requests = db.relationship('User',
                                secondary=requests,
                                primaryjoin=(requests.c.requester_id == id),
                                secondaryjoin=(requests.c.requested_id == id),
                                backref=db.backref('requested', lazy='dynamic'))

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "comments": [comment.to_dict() for comment in self.comments],
            "images": [image.to_dict() for image in self.images],
            "liked_comments": [comment.id for comment in self.comments],
            "liked_images": [image.id for image in self.images],
            "posts": len(self.images),
            "following": [user.id for user in self.following],
            "followers": [user.id for user in self.followers]
        }
