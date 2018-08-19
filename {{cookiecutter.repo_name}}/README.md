# {{cookiecutter.package_name}}

{{cookiecutter.description}}


## First-time setup

Run `./scripts/bootstrap` in a terminal.  This will install
`pip-tools` and sync the dependencies for the first time.


## Running the development server

Run `./scripts/runserver`.


## Dependency management

Dependencies are managed via [pip-tools].

### Adding a dependency

To add a dependency, edit `requirements.in` (or `requirements-dev.in`
for dev dependencies) and add your dependency then run `pip-compile
requirements.in`.

### Syncing dependencies

Run `pip-sync requirements.txt requirements-dev.txt`.


## Migrations

Migrations are managed using [alembic].



[alembic]: http://alembic.zzzcomputing.com/en/latest/
[pip-tools]: https://github.com/jazzband/pip-tools
