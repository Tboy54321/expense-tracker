"""rename User to accounts

Revision ID: 83320db42b57
Revises: 4990e2bb452b
Create Date: 2023-12-22 11:32:56.259811

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '83320db42b57'
down_revision = '4990e2bb452b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=100), nullable=False))
        batch_op.drop_index('username')
        batch_op.create_unique_constraint(None, ['email'])
        batch_op.drop_column('username')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', mysql.VARCHAR(length=50), nullable=False))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_index('email', ['email'], unique=False)
        batch_op.drop_column('username')

    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
