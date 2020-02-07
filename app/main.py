import sentry_sdk
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from . import api, config


def create_app():
    app = FastAPI(
        title=config.APP_NAME,
        version=config.APP_VERSION or "0.1.0",
        debug=config.APP_DEBUG,
    )

    app.include_router(api.router, prefix="/api")
    sentry_sdk.init(dsn=config.SENTRY_DSN)
    return SentryAsgiMiddleware(app)


app = create_app()
