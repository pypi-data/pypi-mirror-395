from pydantic_settings import BaseSettings


class AnyArticleSettings(BaseSettings):
    character_limit: int = 5000
    parser_model: str = "gpt-5-mini"
