from fastapi import FastAPI
from .container import Container
from . import endpoints


def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[endpoints])

    app = FastAPI(
        description='This',
        version='1.0.0',
        title='Storage API',
        contact={'email': 'tobias.schoch@vtxmail.ch'},
        license={
            'name': 'Apache 2.0',
            'url': 'http://www.apache.org/licenses/LICENSE-2.0.html',
        })
    app.container = container
    app.include_router(endpoints.router)
    return app


app = create_app()
