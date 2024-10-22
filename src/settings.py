from functools import cached_property

from cachetools import cached
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str
    APP_HOST: str
    APP_PORT: str
    FILE_STORAGE: str
    SECRET_KEY: str
    ALGORITHM: str
    FILE_SERVER_URL: str
    MEMCACHE_SERVER: str

    @cached_property
    def postgres_url(self):
        return self.DATABASE_URL


    @cached_property
    def app_host(self):
        return self.APP_HOST

    @cached_property
    def app_port(self):
        return self.APP_PORT


    @cached_property
    def file_storage(self):
        return self.FILE_STORAGE

    @cached_property
    def secret_key(self):
        return self.SECRET_KEY

    @cached_property
    def algorithm(self):
        return self.ALGORITHM

    @cached_property
    def memcache_server(self):
        return self.MEMCACHE_SERVER

    @cached_property
    def file_server_url(self):
        return self.FILE_SERVER_URL

settings = Settings()
