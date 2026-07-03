from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # OpenAI
    OPENAI_API_KEY: str

    # Models
    MODEL_PLANNER: str
    MODEL_SPECIALIST: str
    MODEL_CRITIC: str
    MODEL_COMMITTEE: str

    # Future Database
    DATABASE_URL: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()