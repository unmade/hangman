from fastapi import FastAPI

from . import config, monitoring


def create_app():
    app = FastAPI(
        title=config.APP_NAME,
        version=config.APP_VERSION or "0.1.0",
        debug=config.APP_DEBUG,
    )
    include_routes(app)
    return app


def include_routes(app: FastAPI) -> None:
    app.include_router(monitoring.router, prefix="/api", tags=["monitoring"])


app = create_app()
