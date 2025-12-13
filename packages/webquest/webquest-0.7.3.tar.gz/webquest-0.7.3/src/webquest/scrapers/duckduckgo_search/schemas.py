from pydantic import BaseModel


class DuckDuckGoSearchRequest(BaseModel):
    query: str


class Page(BaseModel):
    site: str
    url: str
    title: str
    description: str


class DuckDuckGoSearchResponse(BaseModel):
    pages: list[Page]
