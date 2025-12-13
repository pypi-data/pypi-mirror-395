from pydantic import BaseModel


class AnyArticleRequest(BaseModel):
    url: str


class AnyArticleResponse(BaseModel):
    publisher: str
    title: str
    published_at: str
    authors: list[str]
    content: str
