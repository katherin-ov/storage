"""create tables

Revision ID: 9ac917e0c9d2
Revises: 
Create Date: 2026-01-23 21:28:10.757872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '9ac917e0c9d2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('domain_events',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('operation_id', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('payload', sa.JSON(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('locations',
    sa.Column('location_id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('is_available', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('location_id')
    )
    op.create_table('products',
    sa.Column('product_id', sa.String(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('weight', sa.Integer(), nullable=False),
    sa.Column('id_position', sa.Integer(), nullable=False),
    sa.Column('dimensions', sa.JSON(), nullable=True),
    sa.Column('location_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['locations.location_id'], ),
    sa.PrimaryKeyConstraint('product_id')
    )
    op.create_table('storage_operations',
    sa.Column('operation_id', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('product_id', sa.String(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('order_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.product_id'], ),
    sa.PrimaryKeyConstraint('operation_id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('storage_operations')
    op.drop_table('products')
    op.drop_table('locations')
    op.drop_table('domain_events')
