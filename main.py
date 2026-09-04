from fastapi import FastAPI

from app.routes.moderate import router as moderate_router

app = FastAPI(title="Модерация объявлений")
app.include_router(moderate_router)
