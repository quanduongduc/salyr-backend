from typing import Any

from pydantic import BaseSettings, RedisDsn, root_validator

from helpers.constants import Environment


class Config(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALG: str
    
    SITE_DOMAIN: str = "myapp.com"

    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str = 3306
    DB_NAME: str

    REDIS_PASSWORD: str
    REDIS_HOST: str = 'redis'
    REDIS_PORT: int = 6379  # Default Redis port

    ENVIRONMENT: Environment = Environment.PRODUCTION

    SENTRY_DSN: str | None

    CORS_ORIGINS: list[str]
    CORS_ORIGINS_REGEX: str | None
    CORS_HEADERS: list[str]

    APP_VERSION: str = "1"

    @property
    def redis_url(self) -> RedisDsn:
        return RedisDsn.build(password=self.REDIS_PASSWORD, port=self.REDIS_PORT, host=self.REDIS_HOST, scheme='redis')

    @property
    def mysql_dsn(self):
        connection_string = f"mysql+pymysql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return connection_string

    @root_validator(skip_on_failure=True)
    def validate_sentry_non_local(cls, data: dict[str, Any]) -> dict[str, Any]:
        if data["ENVIRONMENT"].is_deployed and not data["SENTRY_DSN"]:
            raise ValueError("Sentry is not set")

        return data


settings = Config()

app_configs: dict[str, Any] = {"title": "App API"}
if settings.ENVIRONMENT.is_deployed:
    app_configs["root_path"] = f"/v{settings.APP_VERSION}"

if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None  # hide docs
