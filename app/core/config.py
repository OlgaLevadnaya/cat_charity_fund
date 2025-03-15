from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    description: str = (
        'Приложение для Благотворительного '
        'фонда поддержки котиков QRKot'
    )
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()
