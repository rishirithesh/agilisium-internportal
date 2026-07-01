"""add pre_registrations table

Revision ID: 0002_add_pre_registrations
Revises: 0001_add_invitation_pending
Create Date: 2026-07-01 00:10:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0002_add_pre_registrations'
down_revision = '0001_add_invitation_pending'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'pre_registrations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True, index=True),
        sa.Column('otp_hash', sa.String(length=255), nullable=True),
        sa.Column('otp_expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('verified', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('attempts', sa.Integer(), nullable=False, server_default='0'),
    )


def downgrade() -> None:
    op.drop_table('pre_registrations')
