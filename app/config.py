import contextlib
from fastapi import FastAPI
from app.db.script import initialize_database


def __startup():
    initialize_database()


def __shutdown():
    pass


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    """Pre-run and After-run of a FastAPI process"""

    __startup()
    yield
    __shutdown()
