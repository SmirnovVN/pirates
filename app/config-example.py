from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///db.sqlite3"
    external_url: str = "https://dev.ru"
    debug: bool = False
    token: str = "my_dev_secret"
    ship_name: str = "Javaython"


settings = Settings()
