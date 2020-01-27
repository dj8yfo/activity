"""gemcutters prism

Revision ID: 34c052edb7e9
Revises: 
Create Date: 2020-01-21 15:56:50.949081

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34c052edb7e9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('addresses',
    sa.Column('postal_code', sa.Integer(), nullable=False),
    sa.Column('region', sa.String(length=5), nullable=True),
    sa.Column('city', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('postal_code')
    )
    op.create_table('boutiques',
    sa.Column('slug_id', sa.String(length=200), nullable=False),
    sa.Column('title', sa.String(length=120), nullable=True),
    sa.Column('category', sa.String(length=20), nullable=True),
    sa.Column('street_address', sa.String(length=60), nullable=True),
    sa.Column('postal_code', sa.Integer(), nullable=True),
    sa.Column('reviews', sa.Integer(), nullable=True),
    sa.Column('phone', sa.String(length=40), nullable=True),
    sa.Column('comment_address', sa.String(length=60), nullable=True),
    sa.Column('image_url', sa.String(length=120), nullable=True),
    sa.Column('website', sa.String(length=350), nullable=True),
    sa.Column('schedule', sa.String(length=300), nullable=True),
    sa.Column('about', sa.String(length=400), nullable=True),
    sa.ForeignKeyConstraint(['postal_code'], ['addresses.postal_code'], ),
    sa.PrimaryKeyConstraint('slug_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('boutiques')
    op.drop_table('addresses')
    # ### end Alembic commands ###
