from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    description: str = 'Благотворительный фонд помощи котам'
    database_url: str = 'sqlite+aiosqlite:///./qrkot.db'
    secret: str = '7f3c9a82e1d54b6f91c8a73e4d2f6b10'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
