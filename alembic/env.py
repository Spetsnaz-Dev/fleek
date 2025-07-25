from logging.config import fileConfig
import os

from sqlalchemy import pool
from alembic import context

# --- Custom: Import your models ---
from sqlmodel import SQLModel
from app.models.job import Job  # Make sure this import matches your code!

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target_metadata for 'autogenerate' support
target_metadata = SQLModel.metadata

def get_url():
    # Use env var DATABASE_URL if available, else fall back to alembic.ini
    return os.getenv("DATABASE_URL") or config.get_main_option("sqlalchemy.url")

def run_migrations_offline():
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

def run_migrations_online():
    url = get_url()
    connectable = create_async_engine(url, poolclass=pool.NullPool)

    async def do_run_migrations(connection):
        await connection.run_sync(
            lambda sync_conn: context.configure(
                connection=sync_conn,
                target_metadata=target_metadata,
                compare_type=True,
            )
        )
        async with context.begin_transaction():
            await context.run_migrations()

    async def async_main():
        async with connectable.connect() as connection:
            await do_run_migrations(connection)

    asyncio.run(async_main())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
