import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, create_engine # Added create_engine
from sqlalchemy import pool

from alembic import context

# Correctly set up sys.path to find modules in the 'backend' directory
# Assuming env.py is in backend/alembic, '..' goes to backend/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import Base from your database module and all models
from database import Base, DATABASE_URL # Assuming database.py is in backend/
# Option 1: Import all models explicitly if you have a central models module
import models # Assuming models.py is in backend/

# Option 2: If models are scattered or you want to be explicit (less common with Base)
# from models.user import User # Example
# from models.chat import Chat # Example
# ... and so on for all your models

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata # Point to your Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Use DATABASE_URL from environment or fall back to alembic.ini configuration
    url = DATABASE_URL or config.get_main_option("sqlalchemy.url")
    if not url:
        raise ValueError("sqlalchemy.url is not set in alembic.ini and DATABASE_URL environment variable is not set.")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Use DATABASE_URL from environment for online mode
    db_url_to_use = DATABASE_URL
    if not db_url_to_use:
        # Fallback to what's in alembic.ini if DATABASE_URL env var is not set
        # This might happen if running alembic commands outside an env where .env is loaded
        db_url_to_use = config.get_main_option("sqlalchemy.url")
    
    if not db_url_to_use:
        raise ValueError("DATABASE_URL environment variable is not set and sqlalchemy.url is not configured in alembic.ini.")

    # Create engine explicitly with DATABASE_URL
    # The engine_from_config approach is also valid if alembic.ini's sqlalchemy.url is %DATABASE_URL%
    # and the env var is correctly picked up by ConfigParser. This is more direct.
    connectable = create_engine(db_url_to_use, poolclass=pool.NullPool)


    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
