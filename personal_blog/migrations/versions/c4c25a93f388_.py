"""empty message

Revision ID: c4c25a93f388
Revises: 91b0df508748
Create Date: 2024-11-09 03:23:19.213466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4c25a93f388'
down_revision = '91b0df508748'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(length=140), nullable=False))
        batch_op.add_column(sa.Column('content', sa.Text(), nullable=False))
        batch_op.alter_column('timestamp',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_column('body')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('body', sa.VARCHAR(length=140), nullable=False))
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('timestamp',
               existing_type=sa.DATETIME(),
               nullable=False)
        batch_op.drop_column('content')
        batch_op.drop_column('title')

    # ### end Alembic commands ###