from fastapi import FastAPI

import database  # noqa: F401
from api import routers

# setup_logging()

app = FastAPI()


for routes in routers:
    app.include_router(routes)
