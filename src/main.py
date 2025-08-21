from fastapi import FastAPI

from src.task.router import task_router

app = FastAPI()

app.include_router(
    task_router,
)
