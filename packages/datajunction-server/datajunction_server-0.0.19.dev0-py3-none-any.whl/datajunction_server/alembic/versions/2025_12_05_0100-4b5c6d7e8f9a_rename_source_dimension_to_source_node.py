"""Rename source_dimension_node_id to source_node_id

This change allows the dimension_reachability table to store reachability
from ALL nodes (metrics, sources, transforms, etc.) to dimensions,
not just dimension-to-dimension relationships.

Revision ID: 4b5c6d7e8f9a
Revises: 3a4b5c6d7e8f
Create Date: 2025-12-05 01:00:00.000000+00:00
"""

from alembic import op

revision = "4b5c6d7e8f9a"
down_revision = "3a4b5c6d7e8f"
branch_labels = None
depends_on = None


def upgrade():
    # Drop old indexes and constraints
    op.drop_index("idx_dimension_reachability_source", "dimension_reachability")
    op.drop_constraint(
        "uq_dimension_reachability_source_target",
        "dimension_reachability",
        type_="unique",
    )

    # Rename column
    op.alter_column(
        "dimension_reachability",
        "source_dimension_node_id",
        new_column_name="source_node_id",
    )

    # Recreate index and constraint with new column name
    op.create_index(
        "idx_dimension_reachability_source",
        "dimension_reachability",
        ["source_node_id"],
    )
    op.create_unique_constraint(
        "uq_dimension_reachability_source_target",
        "dimension_reachability",
        ["source_node_id", "target_dimension_node_id"],
    )


def downgrade():
    # Drop new indexes and constraints
    op.drop_index("idx_dimension_reachability_source", "dimension_reachability")
    op.drop_constraint(
        "uq_dimension_reachability_source_target",
        "dimension_reachability",
        type_="unique",
    )

    # Rename column back
    op.alter_column(
        "dimension_reachability",
        "source_node_id",
        new_column_name="source_dimension_node_id",
    )

    # Recreate original index and constraint
    op.create_index(
        "idx_dimension_reachability_source",
        "dimension_reachability",
        ["source_dimension_node_id"],
    )
    op.create_unique_constraint(
        "uq_dimension_reachability_source_target",
        "dimension_reachability",
        ["source_dimension_node_id", "target_dimension_node_id"],
    )

