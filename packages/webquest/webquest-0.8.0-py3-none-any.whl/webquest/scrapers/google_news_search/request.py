from pydantic import BaseModel


class GoogleNewsSearchRequest(BaseModel):
    query: str
