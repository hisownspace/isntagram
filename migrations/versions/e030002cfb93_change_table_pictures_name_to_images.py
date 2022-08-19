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

    op.alter_column('comments',
                    column_name='picture_id',
                    new_column_name='image_id',
                    existing_type=sa.Integer(),
                    existing_nullable=False)
    with op.batch_alter_table('comments', naming_convention={ "fk": "fk_comments_picture_id_pictures" }) as batch_op:
        batch_op.drop_constraint("fk_comments_picture_id_pictures", type_="foreignkey")
        batch_op.create_foreign_key(
            constraint_name="fk_comments_image_id_images",
            referent_table="images",
            local_cols=["image_id"],
            remote_cols=["id"]
        )
#     with op.batch_alter_table('tagged_image', naming_convention={ "fk": "fk_tagged_image_picture_id_pictures" }) as batch_op:
        # batch_op.drop_constraint("fk_tagged_image_picture_id_pictures", type_="foreignkey")
        # batch_op.create_foreign_key(
            # constraint_name="fk_tagged_image_image_id_images",
            # referent_table="images",
            # local_cols=["image_id"],
            # remote_cols=["id"]
        # )
    # with op.batch_alter_table('liked_image', naming_convention={ "fk": "fk_liked_image_picture_id_pictures" }) as batch_op:
        # batch_op.drop_constraint("fk_liked_image_picture_id_pictures", type_="foreignkey")
        # batch_op.create_foreign_key(
            # constraint_name="fk_liked_image_image_id_images",
            # referent_table="images",
            # local_cols=["image_id"],
            # remote_cols=["id"]
        # )
    op.rename_table('pictures', 'images')
    # ### end alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.rename_table('tagged_image', 'tagged_picture')
    op.rename_table('liked_image', 'liked_picture')
    op.rename_table('images', 'pictures')
    op.alter_column('comments',
                    column_name='image_id',
                    new_column_name='picture_id', 
                    existing_type=sa.Integer(),
                    existing_nullable=False)
    # ### end Alembic commands ###
