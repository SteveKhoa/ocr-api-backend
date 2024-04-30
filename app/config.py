import contextlib
from fastapi import FastAPI


def __startup():
    pass


def __shutdown():
    pass


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    """Pre-run and After-run of a FastAPI process"""

    __startup()
    yield
    __shutdown()
