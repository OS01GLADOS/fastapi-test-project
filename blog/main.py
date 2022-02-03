from fastapi import FastAPI

from blog import models
from blog.routers import blog, user, authentication
from blog.database import engine


app = FastAPI()

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)


@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event('shutdown')
async def shutdown():
    await engine.dispose()
