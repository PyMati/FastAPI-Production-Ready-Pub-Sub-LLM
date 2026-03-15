from fastapi import FastAPI

import database  # noqa: F401 | This import is needed to initialize the database connection and make sure the models are registered.
from api import routers

# setup_logging()

app = FastAPI()


for routes in routers:
    app.include_router(routes)
