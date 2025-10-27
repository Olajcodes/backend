"""alter user table

Revision ID: 1a64f6ecf08a
Revises: 
Create Date: 2025-10-27 14:25:07.906812

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a64f6ecf08a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    ALTER TABLE users
    ADD COLUMN userType varchar(100) DEFAULT "student" ENUM("student", "admin")
""")
    pass


def downgrade() -> None:
    op.execute("""
    ALTER TABLE users
    DROP COLUMN userType
""")
    pass
