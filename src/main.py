from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi.responses import HTMLResponse

import sentry_sdk
from fastapi import Depends, FastAPI
from redis import asyncio as aioredis
from starlette.middleware.cors import CORSMiddleware

from db import redis
from helpers.utils import JWTBearer
from routers import auth, users, artists, albums, songs, playlists, search
from config.config import app_configs, settings


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # Startup
    pool = aioredis.ConnectionPool.from_url(
        settings.redis_url, max_connections=10, decode_responses=True
    )
    redis.redis_client = aioredis.Redis(connection_pool=pool)
    print(redis.redis_client)
    yield

    # Shutdown
    await redis.redis_client.close()


app = FastAPI(**app_configs)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)

if settings.ENVIRONMENT.is_deployed:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
    )


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", include_in_schema=False, response_class=HTMLResponse)
async def get_home():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Beautiful FastAPI Page</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f7f7f7;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                text-align: center;
            }
            .button {
                display: inline-block;
                padding: 10px 20px;
                background-color: #3498db;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                text-decoration: none;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            .button:hover {
                background-color: #2980b9;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to a Beautiful Salyr Backend &#x1F351; &#127825;</h1>
            <p>Click the button below to access API DOCS:</p>
            <a class="button" href="/docs">Explore</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


app.include_router(
    auth.router, prefix="/auth", tags=["Authentication and Registration"]
)

app.include_router(users.router, dependencies=[Depends(
    JWTBearer())], prefix="/users", tags=["User Profile"])
app.include_router(artists.router, dependencies=[Depends(
    JWTBearer())], prefix="/artists", tags=["Artists"])
app.include_router(albums.router, dependencies=[Depends(
    JWTBearer())], prefix="/albums", tags=["Albums"])
app.include_router(songs.router, dependencies=[Depends(
    JWTBearer())], prefix="/songs", tags=["Songs"])
app.include_router(playlists.router, dependencies=[Depends(
    JWTBearer())], prefix="/playlists", tags=["Playlists"])
app.include_router(search.router, dependencies=[Depends(
    JWTBearer())], prefix="/search", tags=["Search"])
