from pydantic import BaseModel


class AnyArticleResponse(BaseModel):
    publisher: str
    title: str
    published_at: str
    authors: list[str]
    content: str
