"""Add investment amount constraints

Revision ID: f96369f26562
Revises: 968ed570978e
Create Date: 2026-10-08 22:17:07.318038

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'f96369f26562'
down_revision = '968ed570978e'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('charityproject', schema=None) as batch_op:
        batch_op.create_check_constraint(
            'check_charityproject_invested_amount_range',
            'invested_amount >= 0 AND invested_amount <= full_amount',
        )

    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.create_check_constraint(
            'check_donation_invested_amount_range',
            'invested_amount >= 0 AND invested_amount <= full_amount',
        )


def downgrade():
    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.drop_constraint(
            'check_donation_invested_amount_range',
            type_='check',
        )

    with op.batch_alter_table('charityproject', schema=None) as batch_op:
        batch_op.drop_constraint(
            'check_charityproject_invested_amount_range',
            type_='check',
        )
