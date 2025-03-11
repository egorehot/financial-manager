"""create tables

Revision ID: 4892272343b3
Revises:
Create Date: 2025-03-11 12:02:01.083965

"""

import sqlalchemy as sa
from alembic import op


revision = "4892272343b3"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.Integer(),
            server_default=sa.text("(strftime('%s', 'now'))"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.Integer(),
            server_default=sa.text("(strftime('%s', 'now'))"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["categories.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "transactors",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.Integer(),
            server_default=sa.text("(strftime('%s', 'now'))"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.Integer(),
            server_default=sa.text("(strftime('%s', 'now'))"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "transactions",
        sa.Column("date", sa.Integer(), nullable=False),
        sa.Column("type", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("currency", sa.String(), nullable=False),
        sa.Column("transactor_id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.Integer(),
            server_default=sa.text("(strftime('%s', 'now'))"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.Integer(),
            server_default=sa.text("(strftime('%s', 'now'))"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
        ),
        sa.ForeignKeyConstraint(
            ["transactor_id"],
            ["transactors.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("transactions")
    op.drop_table("transactors")
    op.drop_table("categories")
