"""Add BestEfforts

Revision ID: d47dde3b72c8
Revises: ecc82164f561
Create Date: 2022-03-09 15:07:14.254561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd47dde3b72c8'
down_revision = 'ecc82164f561'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('best_efforts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('activity_id', sa.Integer(), nullable=True),
    sa.Column('athlete_id', sa.Integer(), nullable=True),
    sa.Column('elapsed_time', sa.Integer(), nullable=True),
    sa.Column('moving_time', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.String(length=50), nullable=True),
    sa.Column('start_date_local', sa.String(length=50), nullable=True),
    sa.Column('distance', sa.Integer(), nullable=True),
    sa.Column('start_index', sa.Integer(), nullable=True),
    sa.Column('end_index', sa.Integer(), nullable=True),
    sa.Column('pr_rank', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['activity_id'], ['activities.id'], ),
    sa.ForeignKeyConstraint(['athlete_id'], ['athletes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('best_efforts')
    # ### end Alembic commands ###