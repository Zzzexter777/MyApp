from pydantic_settings import BaseSettings, SettingsConfigDict

class DBSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: int
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10

    DB_NAME_MIGRATION: str

    model_config = SettingsConfigDict(
        env_file="src/settings/.env",
    )

db_settings = DBSettings()

def get_db_url():
    return f"postgresql+asyncpg://{db_settings.DB_USER}:{db_settings.DB_PASSWORD}@{db_settings.DB_HOST}:{db_settings.DB_PORT}/{db_settings.DB_NAME}"

def get_db_migration_url():
    return f"postgresql+asyncpg://{db_settings.DB_USER}:{db_settings.DB_PASSWORD}@{db_settings.DB_HOST}:{db_settings.DB_PORT}/{db_settings.DB_NAME_MIGRATION}"


