"""updated models

Revision ID: 406b99feadf9
Revises: e535ad4dc788
Create Date: 2023-11-21 13:10:38.874659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '406b99feadf9'
down_revision = 'e535ad4dc788'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('album', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_flagged', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('album', schema=None) as batch_op:
        batch_op.drop_column('is_flagged')

    # ### end Alembic commands ###
