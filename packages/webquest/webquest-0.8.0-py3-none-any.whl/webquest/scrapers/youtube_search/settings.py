from pydantic_settings import BaseSettings


class YouTubeSearchSettings(BaseSettings):
    result_limit: int = 10
    character_limit: int = 1000
