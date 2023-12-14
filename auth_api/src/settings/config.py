import os
from logging import config as logging_config

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from settings.logger import LOGGING

logging_config.dictConfig(LOGGING)


class RedisSettings(BaseSettings):
    host: str = '127.0.0.1'
    port: int = 6379
    model_config = SettingsConfigDict(env_prefix='redis_')


class PostgresSettings(BaseSettings):
    host: str = '127.0.0.1'
    port: int = 5432
    user: str = 'postgres'
    password: str = 'postgres'
    db: str = 'postgres'
    model_config = SettingsConfigDict(env_prefix='postgres_')


class CommonSettings(BaseSettings):
    project_name: str = 'auth'
    base_dir: str = Field(
        default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    secret_key: str = 'secret'
    access_token_ttl: int = 300
    refresh_token_ttl: int = 10000
    request_rate_limit: int = 15


class OAuthYandexSettings(BaseSettings):
    client_id: str = 'ef3fe64262ac40a29beef2431669a261'
    client_secret: str = 'dd4fb71e89ff4f4ea19752fe6666e01c'
    token_url: str = 'https://oauth.yandex.ru/token'
    user_info_url: str = 'https://login.yandex.ru/info'
    model_config = SettingsConfigDict(env_prefix='yandex_')
