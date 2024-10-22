import traceback
from contextlib import asynccontextmanager
from typing import AsyncIterator

import aioredis
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi_cache import FastAPICache
from fastapi_cache.backends.memcached import MemcachedBackend
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from src.router.files import file_router
from src.settings import settings
from src.unit_of_work import UnitOfWork
from src.utils.exceptions import ResultNotFound, FileSizeExceeded
import memcache

app = FastAPI(
    title="E-notGPT. Files.",
)

app.include_router(file_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    client = memcache.Client([settings.memcache_server], debug=0)
    FastAPICache.init(MemcachedBackend(client), prefix="fastapi-cache")
    uow = UnitOfWork()
    async with uow:
        await uow.init_db()


@app.exception_handler(ResultNotFound)
async def unicorn_exception_handler(request: Request, exc: ResultNotFound):
    return JSONResponse(
        status_code=404,
        content={"status": False, "message": "Запрашиваемый ресурс не найден"},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"status": False, "detail": exc.errors(), "body": exc.body},
    )


@app.exception_handler(FileSizeExceeded)
async def validation_exception_handler(request: Request, exc: FileSizeExceeded):
    return JSONResponse(
        status_code=403,
        content={"status": False, "message": "Допустимый размер файла превышен"},
    )


@app.exception_handler(Exception)
async def internal_server_error_handler(request: Request, exc: Exception):
    error_trace = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))

    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal Server Error",
            "detail": error_trace
        },
    )