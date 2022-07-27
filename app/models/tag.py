from datetime import datetime
from .db import db

tagged_image = db.Table('tagged_image',
    db.Column('tag_id',
                db.Integer,
                db.ForeignKey("tags.id"),
                nullable=False),
    db.Column('image_id',
                db.Integer,
                db.ForeignKey("images.id"),
                nullable=False)
        )

class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

    images = db.relationship("Image",
                                secondary=tagged_image,
                                back_populates="tags")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "images": [(image.id, image.url) for image in self.images]
        }