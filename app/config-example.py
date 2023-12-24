from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    external_url: str = "https://dev.ru"
    debug: bool = False
    send_commands: bool = False
    token: str = "my_dev_secret"


settings = Settings()
