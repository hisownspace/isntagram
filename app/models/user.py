from .db import db
from .comment import liked_comment
from .image import liked_picture
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


followers = db.Table('followers',
    db.Column('follower_id',
                db.Integer,
                db.ForeignKey("users.id"),
                nullable=False),
    db.Column('followed_id',
                db.Integer,
                db.ForeignKey('users.id'),
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
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    comments = db.relationship('Comment', back_populates='user')
    pictures = db.relationship('Image', back_populates='user')

    liked_comment = db.relationship('Comment',
                                    secondary=liked_comment,
                                    back_populates='user_like')
    
    liked_picture = db.relationship('Image',
                                    secondary=liked_picture,
                                    back_populates='user_like')
    
    followed = db.relationship('User',
                                secondary=followers,
                                primaryjoin=(followers.c.follower_id == id),
                                secondaryjoin=(followers.c.followed_id == id),
                                backref=db.backref('followers', lazy='dynamic'),
                                )


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
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
