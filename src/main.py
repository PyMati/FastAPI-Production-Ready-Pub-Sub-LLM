from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import database  # noqa: F401 | This import is needed to initialize the database connection and make sure the models are registered.
from api import routers
from config import config
from middleware import CSRFMiddleware

# setup_logging()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[config.CSRF_HEADER_NAME],
)
app.add_middleware(CSRFMiddleware)


for routes in routers:
    app.include_router(routes, prefix="/api")
