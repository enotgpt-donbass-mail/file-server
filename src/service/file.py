import hashlib
import os
from http.client import HTTPException
from pathlib import Path

from fastapi import UploadFile
from fastapi.security import HTTPAuthorizationCredentials
from starlette.responses import FileResponse, JSONResponse

from src.schemas.file import FileUploadOutput, DataFile, AllFilesOutput
from src.settings import settings
from src.unit_of_work import UnitOfWork
from src.utils.Authorization import Authorization
from src.utils.exceptions import FileSizeExceeded


class FileUpload(Authorization):
    def __init__(self, uow: UnitOfWork, file: UploadFile, token: HTTPAuthorizationCredentials, **kwargs):
        super().__init__(token, **kwargs)
        self.uow = uow
        self.file = file
        self.filename = self.file.filename
        self.extension = self._get_extension()
        self.hash = self._hash_name()
        self.save_path = settings.file_storage + self.TYPE_NAME
        self._extensions()

        if self._file_size() >= self.MAX_FILE_SIZE * 1024 * 1024:
            raise FileSizeExceeded

    MAX_FILE_SIZE: int
    TYPE_NAME: str
    AVAILABLE_EXTENSIONS: list[str]

    def _file_size(self):
        return self.file.size

    def _get_extension(self):
        return Path(self.filename).suffix

    def _hash_name(self):
        return (salt := os.urandom(16)).hex() + ':' + hashlib.pbkdf2_hmac('sha256', self.filename.encode(),
                                                                          salt, 100000).hex()[:64] + self.extension

    def _generate_url(self):
        return settings.file_server_url + "files/" + self.TYPE_NAME + "/" + self.hash

    def _extensions(self):
        if self.extension not in self.AVAILABLE_EXTENSIONS:
            raise HTTPException(403, f"Extension error. Available: {self.AVAILABLE_EXTENSIONS}")

    async def _save(self):
        os.makedirs(self.save_path, exist_ok=True)
        file_path = os.path.join(self.save_path, self.hash)
        with open(file_path, "wb") as f:
            f.write(await self.file.read())

        return file_path

    async def upload(self):
        file = await self.uow.repositories.file.add_one(
            {
                "name": self.filename,
                "hash": self.hash,
                "path": self.save_path,
                "type": self.TYPE_NAME,
                "user_id": self.user_id
            }
        )
        await self.uow.commit()
        await self._save()
        return FileUploadOutput(url=self._generate_url())


class PhotoFileUploadService(FileUpload):
    MAX_FILE_SIZE = 10
    TYPE_NAME = "photos"
    AVAILABLE_EXTENSIONS = [".jpeg", ".jpg", ".png", ".mpeg", ".ico"]

    def __init__(self, uow: UnitOfWork, file: UploadFile, token: HTTPAuthorizationCredentials, **kwargs):
        super().__init__(uow, file, token, **kwargs)


class VideoFileUploadService(FileUpload):
    MAX_FILE_SIZE = 75
    TYPE_NAME = "videos"
    AVAILABLE_EXTENSIONS = [".mp4", ".mow"]

    def __init__(self, uow: UnitOfWork, file: UploadFile, token: HTTPAuthorizationCredentials, **kwargs):
        super().__init__(uow, file, token, **kwargs)


class AudioFileUploadService(FileUpload):
    MAX_FILE_SIZE = 10
    TYPE_NAME = "audios"
    AVAILABLE_EXTENSIONS = [".mp3", ".wav", ".ogg"]

    def __init__(self, uow: UnitOfWork, file: UploadFile, token: HTTPAuthorizationCredentials, **kwargs):
        super().__init__(uow, file, token, **kwargs)


class DocumentFileUploadService(FileUpload):
    MAX_FILE_SIZE = 5
    TYPE_NAME = "documents"
    AVAILABLE_EXTENSIONS = [".txt", ".pdf", ".env"]

    def __init__(self, uow: UnitOfWork, file: UploadFile, token: HTTPAuthorizationCredentials, **kwargs):
        super().__init__(uow, file, token, **kwargs)


class APKFileUploadService(FileUpload):
    MAX_FILE_SIZE = 65
    TYPE_NAME = "mobiles"
    AVAILABLE_EXTENSIONS = [".apk"]

    def __init__(self, uow: UnitOfWork, file: UploadFile, token: HTTPAuthorizationCredentials, **kwargs):
        super().__init__(uow, file, token, **kwargs)
        self.hash = file.filename


class ResponseFile(Authorization):
    def __init__(self, uow: UnitOfWork,  token: HTTPAuthorizationCredentials = None, **kwargs):
        super().__init__(token, **kwargs)
        self.hashed = None
        self.uow = uow

    TYPE_NAME: str

    def _generate_path(self):
        return settings.file_storage + "/" + self.TYPE_NAME + "/" + self.hashed

    async def _generate_url(self):
        return settings.file_server_url + "files/" + self.TYPE_NAME + "/" + self.hashed

    async def get_file(self, hashed):
        self.hashed = hashed
        file = await self.uow.repositories.file.find_one(hash=self.hashed, is_active=True)
        return FileResponse(self._generate_path())

    async def _map_file_data(self, data):
        self.hashed = data.hash
        return DataFile(
            id = data.id,
            name = data.name,
            hash=data.hash,
            create_date=data.create_date,
            url=await self._generate_url()
        )

    async def get_my_files(self):
        files = await self.uow.repositories.file.find_filtered(user_id=self.user_id, is_active=True)
        return JSONResponse(
            AllFilesOutput(
                items = [
                    await self._map_file_data(file) for file in files
                ]
            ).model_dump(mode='json'))


class PhotoFileResponseService(ResponseFile):
    TYPE_NAME = "photos"

class AudioFileResponseService(ResponseFile):
    TYPE_NAME = "audios"

class VideoFileResponseService(ResponseFile):
    TYPE_NAME = "videos"

class DocumentFileResponseService(ResponseFile):
    TYPE_NAME = "documents"

class APKFileResponseService(ResponseFile):
    TYPE_NAME = "mobiles"