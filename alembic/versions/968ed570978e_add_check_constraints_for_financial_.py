"""Add check constraints for financial amounts

Revision ID: 968ed570978e
Revises: a5247fec96b2
Create Date: 2026-10-08 19:41:22.075794

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '968ed570978e'
down_revision = 'a5247fec96b2'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('charityproject', schema=None) as batch_op:
        batch_op.create_check_constraint(
            'check_charityproject_full_amount_positive',
            'full_amount > 0',
        )

    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.create_check_constraint(
            'check_donation_full_amount_positive',
            'full_amount > 0',
        )


def downgrade():
    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.drop_constraint(
            'check_donation_full_amount_positive',
            type_='check',
        )

    with op.batch_alter_table('charityproject', schema=None) as batch_op:
        batch_op.drop_constraint(
            'check_charityproject_full_amount_positive',
            type_='check',
        )
