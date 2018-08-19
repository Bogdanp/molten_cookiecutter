from molten import App, ResponseRendererMiddleware, Route, SettingsComponent
from molten.contrib.request_id import RequestIdMiddleware
from molten.contrib.sqlalchemy import SQLAlchemyEngineComponent, SQLAlchemyMiddleware, SQLAlchemySessionComponent
from molten.contrib.templates import Templates, TemplatesComponent
from whitenoise import WhiteNoise

from . import settings
from .common import path_to
from .logging import setup_logging


def index(templates: Templates):
    return templates.render("index.html")


def setup_app():
    setup_logging()

    app = App(
        components=[
            SQLAlchemyEngineComponent(),
            SQLAlchemySessionComponent(),
            SettingsComponent(settings),
            TemplatesComponent(path_to("templates")),
        ],

        middleware=[
            RequestIdMiddleware(),
            ResponseRendererMiddleware(),
            SQLAlchemyMiddleware(),
        ],

        routes=[
            Route("/", index),
        ],
    )

    decorated_app = WhiteNoise(app, **settings.strict_get("whitenoise"))
    return decorated_app, app
