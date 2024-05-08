from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel

from app.routers import common, proxy, user
from app.database import engine

from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(_: FastAPI):
    # SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan, root_path="/api/v1")


origins = ["http://localhost:5173", "http://127.0.0.1:5137", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(common.router)
app.include_router(user.router)
app.include_router(proxy.router)


@app.get("/")
def read_root():
    return "Hello, World!"
