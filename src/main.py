from fastapi import FastAPI

from api import routers

# setup_logging()

app = FastAPI()


for routes in routers:
    app.include_router(routes)
