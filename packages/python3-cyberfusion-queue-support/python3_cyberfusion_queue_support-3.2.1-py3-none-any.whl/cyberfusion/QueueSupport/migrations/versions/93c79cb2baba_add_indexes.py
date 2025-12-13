"""Add indexes

Revision ID: 93c79cb2baba
Revises: 2f4316506856
Create Date: 2025-10-03 13:55:00.001141

"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "93c79cb2baba"
down_revision = "2f4316506856"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("queue_item_outcomes", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_queue_item_outcomes_queue_item_id"),
            ["queue_item_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_queue_item_outcomes_queue_process_id"),
            ["queue_process_id"],
            unique=False,
        )

    with op.batch_alter_table("queue_items", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_queue_items_queue_id"), ["queue_id"], unique=False
        )

    with op.batch_alter_table("queue_processes", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_queue_processes_queue_id"), ["queue_id"], unique=False
        )


def downgrade() -> None:
    with op.batch_alter_table("queue_processes", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_queue_processes_queue_id"))

    with op.batch_alter_table("queue_items", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_queue_items_queue_id"))

    with op.batch_alter_table("queue_item_outcomes", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_queue_item_outcomes_queue_process_id"))
        batch_op.drop_index(batch_op.f("ix_queue_item_outcomes_queue_item_id"))
