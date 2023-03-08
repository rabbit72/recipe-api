import fastapi

from .routers import recipes

app = fastapi.FastAPI()
app.include_router(recipes.router)
