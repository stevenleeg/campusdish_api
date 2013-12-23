from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from campusdish_api.models import db
import os

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = db.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    db_url = "postgres://%s:%s@%s:%s/%s" % (
        os.environ['DB_USER'],
        os.environ['DB_PASS'],
        os.environ['DB_HOST'],
        os.environ['DB_PORT'],
        os.environ['DB_NAME'],
    )
    context.configure(url=db_url)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    alembic_conf = config.get_section(config.config_ini_section)
    db_url = "postgres://%s:%s@%s:%s/%s" % (
        os.environ['DB_USER'],
        os.environ['DB_PASS'],
        os.environ['DB_HOST'],
        os.environ['DB_PORT'],
        os.environ['DB_NAME'],
    )
    alembic_conf['sqlalchemy.url'] = db_url

    engine = engine_from_config(
                alembic_conf,
                prefix='sqlalchemy.',
                poolclass=pool.NullPool)

    connection = engine.connect()
    context.configure(
                connection=connection,
                target_metadata=target_metadata
                )

    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

