"""change picture_id column to image_id in liked_image table

Revision ID: 4eeecfcdffc8
Revises: 98d4066f20be
Create Date: 2022-07-25 20:13:41.809235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4eeecfcdffc8'
down_revision = '98d4066f20be'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("liked_image", "picture_id", new_column_name="image_id")


def downgrade():
    op.alter_column("liked_image", "image_id", new_column_name="picture_id")
