from fastapi import FastAPI,Request
from user import routes as AdminRoute
from tortoise.contrib.fastapi import register_tortoise
from configs.connection import DATABASE_URL
from user import api as apiRoute
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
import typing





app=FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(SessionMiddleware, secret_key="some-random-string", max_age=None)
db_url=DATABASE_URL()


# app.include_router(apiRoute.router, prefix="/api")






app.include_router(AdminRoute.router,tags={'Admin'})


register_tortoise(
    app,
    db_url=db_url,
    modules={'models':['user.models']},
    generate_schemas=True,
    add_exception_handlers=True
)


