"""add transcript_json to reports

Revision ID: a1b2c3d4e5f6
Revises: 20a6a425cee7
Create Date: 2026-04-15 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "20a6a425cee7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add transcript_json TEXT column to reports (nullable — legacy rows stay NULL)."""
    op.add_column("reports", sa.Column("transcript_json", sa.Text(), nullable=True))


def downgrade() -> None:
    """Remove transcript_json column from reports."""
    op.drop_column("reports", "transcript_json")
