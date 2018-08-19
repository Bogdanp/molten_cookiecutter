"""isort:skip_file
"""
import os
import sys; sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), ".."))  # noqa

from alembic import context
from {{cookiecutter.package_name}}.app import setup_app
from {{cookiecutter.package_name}}.models import Base
from molten.contrib.sqlalchemy import EngineData

_, app = setup_app()


def run_migrations_online(engine_data: EngineData):
    with engine_data.engine.connect() as connection:
        context.configure(connection=connection, target_metadata=Base.metadata)
        with context.begin_transaction():
            context.run_migrations()


app.injector.get_resolver().resolve(run_migrations_online)()
