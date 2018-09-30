import pytest

from molten import testing
from molten.contrib.sqlalchemy import Session
from {{cookiecutter.package_name}}.app import setup_app


def truncate_all_tables(session: Session):
    table_names = session.execute("""
        select table_name from information_schema.tables
        where table_schema = 'public'
        and table_type = 'BASE TABLE'
        and table_name != 'alembic_version'
    """)
    for (table_name,) in table_names:
        # "truncate" can deadlock so we use delete which is guaranteed not to.
        session.execute(f"delete from {table_name}")
    session.commit()


@pytest.fixture(scope="session")
def app_global():
    _, app = setup_app()
    return app


@pytest.fixture
def app(app_global):
    # This is a little "clever"/piggy. We only want a single instance
    # of the app to ever be created, but we also want to ensure that
    # the DB is cleared after every test hence "app_global" being a
    # session-scoped fixture and this one being test-scoped.
    yield app_global
    resolver = app_global.injector.get_resolver()
    resolver.resolve(truncate_all_tables)()


@pytest.fixture
def client(app):
    return testing.TestClient(app)


@pytest.fixture
def load_component(app):
    def load(annotation):
        def loader(c: annotation):
            return c
        return app.injector.get_resolver().resolve(loader)()
    return load
