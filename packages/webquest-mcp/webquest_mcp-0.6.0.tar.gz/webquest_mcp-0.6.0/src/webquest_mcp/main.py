from typing import Literal

from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import JWTVerifier
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings
from webquest.scrapers import (
    AnyArticleRequest,
    AnyArticleResponse,
    DuckDuckGoSearchRequest,
    DuckDuckGoSearchResponse,
    GoogleNewsSearchRequest,
    GoogleNewsSearchResponse,
    YouTubeSearchRequest,
    YouTubeSearchResponse,
    YouTubeTranscriptRequest,
    YouTubeTranscriptResponse,
)

from webquest_mcp.app_state import app_lifespan, get_app_state


class Settings(BaseSettings):
    auth_secret: SecretStr | None = Field(default=None)
    auth_audience: str | None = Field(default="webquest-mcp")
    transport: Literal[
        "stdio",
        "sse",
        "streamable-http",
    ] = Field(default="stdio")
    port: int = Field(default=8000)


load_dotenv()

settings = Settings()


auth: JWTVerifier | None = None
if settings.auth_secret is not None and settings.auth_audience is not None:
    auth = JWTVerifier(
        public_key=settings.auth_secret.get_secret_value(),
        audience=settings.auth_audience,
        algorithm="HS256",
    )


mcp = FastMCP("WebQuest MCP", lifespan=app_lifespan, auth=auth)


@mcp.tool()
async def any_article(
    request: AnyArticleRequest,
) -> AnyArticleResponse:
    """Get the content of an article given its URL."""
    app_state = get_app_state()
    scraper = app_state.any_article
    response = await scraper.run(request)
    return response


@mcp.tool()
async def duckduckgo_search(
    request: DuckDuckGoSearchRequest,
) -> DuckDuckGoSearchResponse:
    """Search the web using DuckDuckGo given a query."""
    app_state = get_app_state()
    scraper = app_state.duckduckgo_search
    response = await scraper.run(request)
    return response


@mcp.tool()
async def google_news_search(
    request: GoogleNewsSearchRequest,
) -> GoogleNewsSearchResponse:
    """Search for news articles using Google News given a query."""
    app_state = get_app_state()
    scraper = app_state.google_news_search
    response = await scraper.run(request)
    return response


@mcp.tool()
async def youtube_search(
    request: YouTubeSearchRequest,
) -> YouTubeSearchResponse:
    """Search for YouTube videos, channels, posts, and shorts given a query."""
    app_state = get_app_state()
    scraper = app_state.youtube_search
    response = await scraper.run(request)
    return response


@mcp.tool()
async def youtube_transcript(
    request: YouTubeTranscriptRequest,
) -> YouTubeTranscriptResponse:
    """Get the transcript of a YouTube video given its ID."""
    app_state = get_app_state()
    scraper = app_state.youtube_transcript
    response = await scraper.run(request)
    return response


def main() -> None:
    if settings.transport == "stdio":
        mcp.run(transport=settings.transport)
    else:
        mcp.run(transport=settings.transport, port=settings.port)


if __name__ == "__main__":
    main()
