from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_NAME: str

    @property
    def DATABASE_URL_aiosqlite(self):
        return f"sqlite+aiosqlite:///{self.DATABASE_NAME}"
    
    model_config = SettingsConfigDict(env_file=".env", env_prefix="DB_", extra="ignore")

settings = Settings()