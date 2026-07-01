"""add offer_versions and internships tables; add offer_sent_at to referrals

Revision ID: 0004_add_offer_versions_internships
Revises: 0003_add_employee_approved_at
Create Date: 2026-07-01 00:40:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0004_add_offer_versions_internships'
down_revision = '0003_add_employee_approved_at'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'offer_versions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('offer_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('offers.id'), nullable=False, index=True),
        sa.Column('storage_key', sa.String(length=1024), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'internships',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False, index=True),
        sa.Column('referral_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('referrals.id'), nullable=False, index=True),
        sa.Column('offer_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('offers.id'), nullable=False, index=True),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('stipend_amount', sa.String(length=64), nullable=True),
    )

    op.add_column('referrals', sa.Column('offer_sent_at', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column('referrals', 'offer_sent_at')
    op.drop_table('internships')
    op.drop_table('offer_versions')
