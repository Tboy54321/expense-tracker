"""Initial migration

Revision ID: 4d8f54db4258
Revises: d6401ce15488
Create Date: 2023-12-22 14:01:15.289386

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4d8f54db4258'
down_revision = 'd6401ce15488'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.drop_index('username')
        batch_op.create_unique_constraint(None, ['email'])
        batch_op.drop_column('username')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', mysql.VARCHAR(length=50), nullable=False))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_index('username', ['username'], unique=False)
        batch_op.alter_column('email',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=False)

    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
