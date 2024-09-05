"""init

Revision ID: 358679881305
Revises: 
Create Date: 2024-09-05 23:05:07.813860

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "358679881305"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "phonenumbers",
        sa.Column("phone_number", sa.String(length=11), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("username", sa.String(length=20), nullable=False),
        sa.Column("password", sa.String(length=20), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("external_id", sa.String(length=50), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "smscodes",
        sa.Column("code", sa.String(length=6), nullable=False),
        sa.Column("is_used", sa.Boolean(), nullable=False),
        sa.Column("phone_number_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["phone_number_id"],
            ["phonenumbers.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "userts",
        sa.Column("firt_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("update_at", sa.DateTime(), nullable=True),
        sa.Column("last_login", sa.DateTime(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("external_id", sa.String(length=150), nullable=True),
        sa.Column("client_uuid", sa.UUID(), nullable=True),
        sa.Column("phone_number_id", sa.UUID(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["phone_number_id"],
            ["phonenumbers.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "emails",
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["userts.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "jwtokens",
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("issued_at", sa.DateTime(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column(
            "token_type",
            sa.Enum("ACCESS", "REFRESH", name="tokentypeenum"),
            nullable=False,
        ),
        sa.Column("token", sa.String(length=200), nullable=False),
        sa.Column("revoked", sa.Boolean(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["userts.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "socialaccounts",
        sa.Column("provider", sa.String(length=50), nullable=False),
        sa.Column("provider_user_id", sa.String(length=100), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["userts.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("socialaccounts")
    op.drop_table("jwtokens")
    op.drop_table("emails")
    op.drop_table("userts")
    op.drop_table("smscodes")
    op.drop_table("users")
    op.drop_table("phonenumbers")
    # ### end Alembic commands ###
