from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_API_TOKEN: str

    BINANCE_API_KEY: str
    BINANCE_SECRET_KEY: str

    MONGO_URL: str
    MONGO_DB: str

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_FSM_DB: str
    REDIS_JOB_DB: str

    model_config = SettingsConfigDict(env_file='./.env', case_sensitive=True)


settings = Settings()
