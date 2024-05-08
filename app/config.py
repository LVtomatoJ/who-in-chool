from datetime import timedelta
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///database.db"
    echo_sql: bool = True
    test: bool = False
    project_name: str = "who in school?"
    token_secret: str = (
        "3503fafffd9729544732a36791e62f1978e57f1ff3f9900f95e611a5103613a0"
    )
    access_token_expires_delta: timedelta = timedelta(minutes=30)


settings = Settings()
