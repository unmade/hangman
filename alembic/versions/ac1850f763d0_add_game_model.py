"""Add Game model

Revision ID: ac1850f763d0
Revises:
Create Date: 2020-02-07 21:31:56.671523

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ac1850f763d0"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "game",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("game_uid", sa.String(length=32), nullable=True),
        sa.Column("word", sa.String(), nullable=False),
        sa.Column("known_letters", sa.String(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("max_attempts", sa.Integer(), nullable=False),
        sa.Column("attempt_count", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("game_uid"),
    )
    op.create_index(op.f("ix_game_id"), "game", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_game_id"), table_name="game")
    op.drop_table("game")
    # ### end Alembic commands ###