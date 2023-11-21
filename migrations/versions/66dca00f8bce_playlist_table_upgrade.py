"""playlist table upgrade

Revision ID: 66dca00f8bce
Revises: 85e5da4324a6
Create Date: 2023-11-19 11:27:54.158919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66dca00f8bce'
down_revision = '85e5da4324a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('playlist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('playlist_desc', sa.String(length=300), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('playlist', schema=None) as batch_op:
        batch_op.drop_column('playlist_desc')

    # ### end Alembic commands ###