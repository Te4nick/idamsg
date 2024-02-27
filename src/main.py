import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api.routers import v1_router

app = FastAPI()
app.include_router(v1_router)
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
