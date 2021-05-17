"""empty message

Revision ID: 67eb4e468c7f
Revises: 5b055e133fda
Create Date: 2021-05-13 10:45:07.765490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67eb4e468c7f'
down_revision = '5b055e133fda'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('subject', sa.String(length=100), nullable=True),
    sa.Column('comment', sa.String(length=100000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    # ### end Alembic commands ###