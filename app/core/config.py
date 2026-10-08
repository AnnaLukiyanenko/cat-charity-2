from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    description: str = 'Благотворительный фонд помощи котам'
    database_url: str = 'sqlite+aiosqlite:///./qrkot.db'
    secret: str

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
