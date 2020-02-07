from fastapi import FastAPI

from . import api, config


def create_app():
    app = FastAPI(
        title=config.APP_NAME,
        version=config.APP_VERSION or "0.1.0",
        debug=config.APP_DEBUG,
    )
    app.include_router(api.router, prefix="/api")
    return app


app = create_app()
