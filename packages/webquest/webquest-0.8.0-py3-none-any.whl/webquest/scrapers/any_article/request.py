from pydantic import BaseModel


class AnyArticleRequest(BaseModel):
    url: str
