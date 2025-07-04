from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DB_NAME: str="default"
    
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file=".env")
settings = Settings()