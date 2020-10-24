"""add username to workflow

Revision ID: 385401018742
Revises: e2bc6261f314
Create Date: 2020-10-24 16:01:50.304871

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '385401018742'
down_revision = 'e2bc6261f314'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('workflow', sa.Column('username', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_workflow_username'), 'workflow', ['username'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_workflow_username'), table_name='workflow')
    op.drop_column('workflow', 'username')
    # ### end Alembic commands ###
