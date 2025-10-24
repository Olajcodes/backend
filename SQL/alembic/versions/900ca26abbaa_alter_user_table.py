"""alter user table

Revision ID: 900ca26abbaa
Revises: 4a172996f99b
Create Date: 2025-10-23 13:42:21.302120

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '900ca26abbaa'
down_revision: Union[str, Sequence[str], None] = '4a172996f99b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
