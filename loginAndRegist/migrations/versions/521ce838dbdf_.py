"""empty message

Revision ID: 521ce838dbdf
Revises: cef824580cd7
Create Date: 2018-06-25 21:04:19.963519

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '521ce838dbdf'
down_revision = 'cef824580cd7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('category', sa.String(length=255), nullable=True))
    op.add_column('posts', sa.Column('characters', sa.String(length=255), nullable=True))
    op.add_column('posts', sa.Column('director', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'director')
    op.drop_column('posts', 'characters')
    op.drop_column('posts', 'category')
    # ### end Alembic commands ###