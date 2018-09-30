from molten import App, Include, ResponseRendererMiddleware, Route, SettingsComponent
from molten.contrib.request_id import RequestIdMiddleware
from molten.contrib.sqlalchemy import SQLAlchemyEngineComponent, SQLAlchemyMiddleware, SQLAlchemySessionComponent
from molten.contrib.templates import Templates, TemplatesComponent
from molten.openapi import Metadata, OpenAPIHandler, OpenAPIUIHandler
from whitenoise import WhiteNoise

from . import pets, settings
from .common import path_to
from .components.pets import PetManager
from .logging import setup_logging
from .models import ManagerComponent


def index(templates: Templates):
    return templates.render("index.html")


def setup_app():
    setup_logging()

    get_docs = OpenAPIUIHandler()
    get_schema = OpenAPIHandler(
        metadata=Metadata(
            title="Pets",
            description="",
            version="0.0.0",
        ),
    )

    app = App(
        components=[
            ManagerComponent(PetManager),
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
            Route("/_docs", get_docs),
            Route("/_schema", get_schema),
            Route("/", index),
            Include("/v1/pets", pets.routes, namespace="pets"),
        ],
    )

    decorated_app = WhiteNoise(app, **settings.strict_get("whitenoise"))
    return decorated_app, app
