"""alter users table

Revision ID: 83c1e905e291
Revises: bf7878e1ff20
Create Date: 2025-10-27 11:37:04.881981

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83c1e905e291'
down_revision: Union[str, Sequence[str], None] = 'bf7878e1ff20'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        ALTER TABLE users
        ADD COLUMN userType varchar(100) DEFAULT 'student' 
""")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        ALTER TABLE users
        DROP COLUMN userType
""")
    pass
