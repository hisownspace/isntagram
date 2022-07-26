"""change picture_id column in tagged_image table to image_id

Revision ID: 98d4066f20be
Revises: 05bc9889da43
Create Date: 2022-07-25 20:07:01.102670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98d4066f20be'
down_revision = '05bc9889da43'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('tagged_image', 'picture_id', new_column_name='image_id')


def downgrade():
    op.alter_column('tagged_image', 'image_id', new_column_name='picture_id')
