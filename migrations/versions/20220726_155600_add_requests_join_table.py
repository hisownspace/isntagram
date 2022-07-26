"""add requests join table, change followers join table name to follows

Revision ID: 759d2664aa05
Revises: 4eeecfcdffc8
Create Date: 2022-07-26 15:56:00.159292

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '759d2664aa05'
down_revision = '4eeecfcdffc8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('follow_requests',
    sa.Column('requester_id', sa.Integer(), nullable=False),
    sa.Column('requested_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['requested_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['requester_id'], ['users.id'], )
    )
    op.rename_table('followers', 'follows')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('follow_requests')
    op.rename_table("follows", "followers")
    # ### end Alembic commands ###