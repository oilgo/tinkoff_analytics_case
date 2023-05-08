from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from core import models
from apps import router
from core import engine

models.Base.metadata.create_all(engine)

# Инициализация приложения
app = FastAPI(
    title="Рога и копыта partnership")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

# Вывод конечных точек сервисов на интерфейс API
app.include_router(
    router=router)


# Точка входа в приложение
@app.get(
    path="/")
async def main():
    return RedirectResponse(
        url="/docs/")

