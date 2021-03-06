"""change table pictures name to images

Revision ID: e030002cfb93
Revises: 82afa48b2841
Create Date: 2022-07-25 17:18:28.349403

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e030002cfb93'
down_revision = '82afa48b2841'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.rename_table('tagged_picture', 'tagged_image')
    op.rename_table('liked_picture', 'liked_image')
    op.rename_table('pictures', 'images')
    op.alter_column('comments', 'picture_id', nullable=False, new_column_name='image_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.rename_table('tagged_image', 'tagged_picture')
    op.rename_table('liked_image', 'liked_picture')
    op.rename_table('images', 'pictures')
    op.alter_column('comments', 'image_id', nullable=False, new_column_name='picture_id')
    # ### end Alembic commands ###
