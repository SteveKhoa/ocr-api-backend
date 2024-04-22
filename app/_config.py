import contextlib
from fastapi import FastAPI
from app.db.script import initialize_database


def __startup():
    initialize_database()


def __shutdown():
    pass


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    """Pre-run and After-run of FastAPI app

    __startup() executed on every
    """

    __startup()
    yield
    __shutdown()
