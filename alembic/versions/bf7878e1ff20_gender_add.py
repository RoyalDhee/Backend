"""gender add

Revision ID: bf7878e1ff20
Revises: 9d319e1cb8a7
Create Date: 2025-10-27 11:23:30.340377

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf7878e1ff20'
down_revision: Union[str, Sequence[str], None] = '9d319e1cb8a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        ALTER TABLE users
        ADD COLUMN gender varchar(100)
""")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        ALTER TABLE users
        DROP COLUMN gender
""")
    pass
