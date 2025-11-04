import secrets

from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    jwt_secret: str = Field(
        min_length=32,
        default_factory=lambda: secrets.token_urlsafe(32),
        description="JWT secret key for token signing",
    )

    jwt_algorithm: str = Field(default="HS256", pattern="^(HS256|HS384|HS512)$")

    database_url: str = Field(
        pattern=r"^postgresql\+psycopg2://[^:]+:[^@]+@[^/]+/[^?]+",
        description="PostgreSQL database URL",
    )

    bcrypt_rounds: int = Field(
        default=12, ge=12, le=18, description="BCrypt rounds for password hashing"
    )

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", case_sensitive=True
    )

    @validator("jwt_secret")
    def validate_jwt_secret(cls, v):
        if v == "changeme" or len(v) < 32:
            raise ValueError(
                "JWT secret must be at least 32 characters long and not use default value"
            )
        return v

    @validator("database_url")
    def validate_database_url(cls, v):
        if "password" in v.lower() and len(v.split(":")) < 4:
            raise ValueError("Database URL appears to have weak credentials")
        return v


settings = Settings()
