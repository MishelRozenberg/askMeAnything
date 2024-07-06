"""Add questions table

Revision ID: 7e9421976de7
Revises: 
Create Date: 2024-07-05 22:03:20.848502

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e9421976de7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("questions",
                    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
                    sa.Column("question_data", sa.String, nullable=False),
                    sa.Column("answer_data", sa.String, nullable=False))


def downgrade() -> None:
    op.drop_table("questions")
