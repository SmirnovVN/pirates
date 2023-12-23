from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    external_url: str = "https://dev.ru"
    debug: bool = True
    token: str = "my_dev_secret"


settings = Settings()
