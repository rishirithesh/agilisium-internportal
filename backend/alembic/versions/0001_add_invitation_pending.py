"""add invitation fields and pending_intern_registrations table

Revision ID: 0001_add_invitation_pending
Revises: 
Create Date: 2026-07-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001_add_invitation_pending'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add columns to referrals table
    op.add_column('referrals', sa.Column('invitation_token_hash', sa.String(length=255), nullable=True))
    op.add_column('referrals', sa.Column('invitation_expires_at', sa.DateTime(timezone=True), nullable=True))

    # Create pending_intern_registrations table
    op.create_table(
        'pending_intern_registrations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('referral_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('referrals.id'), nullable=False, index=True),
        sa.Column('email', sa.String(length=255), nullable=False, index=True),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('entered_details', sa.Text, nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('pending_intern_registrations')
    op.drop_column('referrals', 'invitation_expires_at')
    op.drop_column('referrals', 'invitation_token_hash')
