from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from fastmcp import FastMCP
from hyperbrowser import AsyncHyperbrowser
from openai import AsyncOpenAI
from webquest.browsers import Hyperbrowser
from webquest.scrapers import (
    AnyArticle,
    DuckDuckGoSearch,
    GoogleNewsSearch,
    YouTubeSearch,
    YouTubeTranscript,
)

from webquest_mcp.settings import get_settings


@dataclass
class AppState:
    any_article: AnyArticle
    duckduckgo_search: DuckDuckGoSearch
    google_news_search: GoogleNewsSearch
    youtube_search: YouTubeSearch
    youtube_transcript: YouTubeTranscript


_app_state: AppState | None = None


def get_app_state() -> AppState:
    global _app_state
    if _app_state is None:
        raise RuntimeError("App state is not initialized.")
    return _app_state


@asynccontextmanager
async def app_lifespan(_: FastMCP) -> AsyncIterator[None]:
    global _app_state
    settings = get_settings()

    if settings.hyperbrowser_api_key is None:
        raise RuntimeError("Hyerpbrowser API key is not set in settings.")
    hyperbrowser_client = AsyncHyperbrowser(
        api_key=settings.hyperbrowser_api_key.get_secret_value(),
    )

    if settings.openai_api_key is None:
        raise RuntimeError("OpenAI API key is not set in settings.")
    openai_client = AsyncOpenAI(
        api_key=settings.openai_api_key.get_secret_value(),
    )

    browser = Hyperbrowser(client=hyperbrowser_client)
    any_article = AnyArticle(browser=browser, client=openai_client)
    duckduckgo_search = DuckDuckGoSearch(browser=browser)
    google_news_search = GoogleNewsSearch(browser=browser)
    youtube_search = YouTubeSearch(browser=browser)
    youtube_transcript = YouTubeTranscript(browser=browser)
    app_state = AppState(
        any_article=any_article,
        duckduckgo_search=duckduckgo_search,
        google_news_search=google_news_search,
        youtube_search=youtube_search,
        youtube_transcript=youtube_transcript,
    )
    _app_state = app_state
    try:
        yield
    finally:
        pass
