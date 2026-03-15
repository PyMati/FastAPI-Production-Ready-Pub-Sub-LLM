from fastapi import FastAPI

from api import routers

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


for routes in routers:
    app.include_router(routes)
