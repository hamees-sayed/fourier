"""updated models

Revision ID: f482a187096d
Revises: 66dca00f8bce
Create Date: 2023-11-21 12:54:44.588489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f482a187096d'
down_revision = '66dca00f8bce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('album', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_flagged', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('album', schema=None) as batch_op:
        batch_op.drop_column('is_flagged')

    # ### end Alembic commands ###
