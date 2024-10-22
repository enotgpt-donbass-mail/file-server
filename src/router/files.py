from typing import Annotated

import memcache
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_cache import FastAPICache
from fastapi_cache.backends.memcached import MemcachedBackend
from fastapi_cache.decorator import cache

from src.service.file import PhotoFileUploadService, VideoFileUploadService, AudioFileUploadService, \
    DocumentFileUploadService, PhotoFileResponseService, VideoFileResponseService, AudioFileResponseService, \
    DocumentFileResponseService, APKFileUploadService, APKFileResponseService
from src.unit_of_work import UnitOfWork

file_router = APIRouter()
security = HTTPBearer()


@file_router.post("/upload/photo", tags=["Upload"])
async def upload_photo(uow: Annotated[UnitOfWork, Depends(UnitOfWork)],
                       file: UploadFile = File(...),
                       token: HTTPAuthorizationCredentials = Depends(security)):
    async with uow:
        return await PhotoFileUploadService(uow, file, token, protected=True, available_roles=['*']).upload()


@file_router.post("/upload/video", tags=["Upload"])
async def upload_video(uow: Annotated[UnitOfWork, Depends(UnitOfWork)],
                       file: UploadFile = File(...),
                       token: HTTPAuthorizationCredentials = Depends(security)):
    async with uow:
        return await VideoFileUploadService(uow, file, token, protected=True, available_roles=['*']).upload()


@file_router.post("/upload/audio", tags=["Upload"])
async def upload_audio(uow: Annotated[UnitOfWork, Depends(UnitOfWork)],
                       file: UploadFile = File(...),
                       token: HTTPAuthorizationCredentials = Depends(security)):
    async with uow:
        return await AudioFileUploadService(uow, file, token, protected=True, available_roles=['*']).upload()


@file_router.post("/upload/document", tags=["Upload"])
async def upload_document(uow: Annotated[UnitOfWork, Depends(UnitOfWork)],
                       file: UploadFile = File(...),
                       token: HTTPAuthorizationCredentials = Depends(security)):
    async with uow:
        return await DocumentFileUploadService(uow, file, token, protected=True, available_roles=['*']).upload()


@file_router.post("/upload/mobile", tags=["Upload"])
async def upload_photo(uow: Annotated[UnitOfWork, Depends(UnitOfWork)],
                       file: UploadFile = File(...),
                       token: HTTPAuthorizationCredentials = Depends(security)):
    async with uow:
        return await APKFileUploadService(uow, file, token, protected=True, available_roles=['*']).upload()

@file_router.get("/files/photos/{hashed}", tags=["Download"])
@cache(expire=60*24*7)
async def files_get_photo(hashed: str, uow: Annotated[UnitOfWork, Depends(UnitOfWork)]):
    async with uow:
        return await PhotoFileResponseService(uow).get_file(hashed)


@file_router.get("/files/videos/{hashed}", tags=["Download"])
@cache(expire=60*24*7)
async def files_get_video(hashed: str, uow: Annotated[UnitOfWork, Depends(UnitOfWork)]):
    async with uow:
        return await VideoFileResponseService(uow).get_file(hashed)


@file_router.get("/files/audios/{hashed}", tags=["Download"])
@cache(expire=60*24*7)
async def files_get_audio(hashed: str, uow: Annotated[UnitOfWork, Depends(UnitOfWork)]):
    async with uow:
        return await AudioFileResponseService(uow).get_file(hashed)


@file_router.get("/files/documents/{hashed}", tags=["Download"])
@cache(expire=60*24*7)
async def files_get_photo(hashed: str, uow: Annotated[UnitOfWork, Depends(UnitOfWork)]):
    async with uow:
        return await DocumentFileResponseService(uow).get_file(hashed)

@file_router.get("/files/mobiles/{hashed}", tags=["Download"])
@cache(expire=60*24*7)
async def files_get_photo(hashed: str, uow: Annotated[UnitOfWork, Depends(UnitOfWork)]):
    async with uow:
        return await APKFileResponseService(uow).get_file(hashed)


@file_router.get("/files/photo/all", tags=["Get all"])
async def photos_all(uow: Annotated[UnitOfWork, Depends(UnitOfWork)],
                     token: HTTPAuthorizationCredentials = Depends(security)):
    async with uow:
        return await PhotoFileResponseService(uow, token, protected=True).get_my_files()


@file_router.get("/files/video/all", tags=["Get all"])
async def videos_all(uow: Annotated[UnitOfWork, Depends(UnitOfWork)],
                     token: HTTPAuthorizationCredentials = Depends(security)):
    async with uow:
        return await VideoFileResponseService(uow, token, protected=True).get_my_files()


@file_router.get("/files/audio/all", tags=["Get all"])
async def audios_all(uow: Annotated[UnitOfWork, Depends(UnitOfWork)],
                     token: HTTPAuthorizationCredentials = Depends(security)):
    async with uow:
        return await AudioFileResponseService(uow, token, protected=True).get_my_files()


@file_router.get("/files/document/all", tags=["Get all"])
async def documents_all(uow: Annotated[UnitOfWork, Depends(UnitOfWork)],
                     token: HTTPAuthorizationCredentials = Depends(security)):
    async with uow:
        return await DocumentFileResponseService(uow, token, protected=True).get_my_files()
