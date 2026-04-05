from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.postgres import PostgresStore

import database  # noqa: F401 | This import is needed to initialize the database connection and make sure the models are registered.
from api import routers
from config import config
from middleware import CSRFMiddleware

with (
    PostgresSaver.from_conn_string(config.MEMORY_DATABASE_URL) as checkpointer,
    PostgresStore.from_conn_string(config.MEMORY_DATABASE_URL) as store,
):
    checkpointer.setup()
    store.setup()

# setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[config.CSRF_HEADER_NAME],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(CSRFMiddleware)


for routes in routers:
    app.include_router(routes, prefix="/api")
