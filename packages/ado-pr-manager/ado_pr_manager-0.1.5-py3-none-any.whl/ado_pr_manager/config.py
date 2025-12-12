from pydantic import Field, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    AZDO_ORG_URL: str
    AZDO_PAT: str
    AZDO_PROJECT: str | None = None
    AZDO_REPO_ID: str | None = Field(
        default=None, validation_alias=AliasChoices("AZDO_REPO_ID", "AZDO_REPO")
    )
    AZDO_DEFAULT_BRANCH: str | None = "main"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
