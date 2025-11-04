import secrets

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    jwt_secret: str = Field(
        min_length=32,
        default_factory=lambda: secrets.token_urlsafe(32),
        description="JWT secret key for token signing",
    )

    jwt_algorithm: str = Field(default="HS256")

    database_url: str = Field(
        pattern=r"^postgresql\+psycopg2://.+$",
        description="PostgreSQL database URL",
    )

    bcrypt_rounds: int = Field(
        default=12, ge=12, le=18, description="BCrypt rounds for password hashing"
    )

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
