from sqlalchemy import Boolean, MetaData, Table, Column, Integer, String, ForeignKey, TIMESTAMP

from datetime import datetime
metadata = MetaData()

role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("type", String, nullable=False),
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("given_name", String, nullable=False),
    Column("surname", String, nullable=False),
    Column("nickname", String, nullable=False),
    Column("email", String, nullable=False),
    Column("hashed_password", String(length=1024), nullable=False),
    Column("role_id", Integer, ForeignKey(role.c.id)),
    Column("registration_date", TIMESTAMP, default=datetime.utcnow),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)