from datetime import datetime
from .db import db

tagged_picture = db.Table('tagged_picture',
    db.Column('tag_id',
                db.Integer,
                db.ForeignKey("tag.id"),
                nullable=False),
    db.Column('picture_id',
                db.Integer,
                db.foreignKey("picture.id"),
                nullable=False)
        )

class Tag(db.model):
    tablename = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    pictures = db.relationship("Picture",
                                secondary=tagged_picture,
                                back_populates="tags")
