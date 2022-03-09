"""Update primary keys for Split, Comment and Kudoser

Revision ID: ecc82164f561
Revises: b635c5d64e11
Create Date: 2022-03-09 14:46:12.615430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecc82164f561'
down_revision = 'b635c5d64e11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.alter_column('activity_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('kudosers', schema=None) as batch_op:
        batch_op.alter_column('activity_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('firstname',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('lastname',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
        batch_op.drop_column('id')

    with op.batch_alter_table('splits', schema=None) as batch_op:
        batch_op.alter_column('activity_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('split',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('is_metric',
               existing_type=sa.BOOLEAN(),
               nullable=False)
        batch_op.drop_column('id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('splits', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.INTEGER(), nullable=False))
        batch_op.alter_column('is_metric',
               existing_type=sa.BOOLEAN(),
               nullable=True)
        batch_op.alter_column('split',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('activity_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('kudosers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.INTEGER(), nullable=False))
        batch_op.alter_column('lastname',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('firstname',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('activity_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.alter_column('activity_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###