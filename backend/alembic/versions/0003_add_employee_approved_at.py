"""add employee_approved_at to referrals

Revision ID: 0003_add_employee_approved_at
Revises: 0002_add_pre_registrations
Create Date: 2026-07-01 00:20:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0003_add_employee_approved_at'
down_revision = '0002_add_pre_registrations'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('referrals', sa.Column('employee_approved_at', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column('referrals', 'employee_approved_at')
