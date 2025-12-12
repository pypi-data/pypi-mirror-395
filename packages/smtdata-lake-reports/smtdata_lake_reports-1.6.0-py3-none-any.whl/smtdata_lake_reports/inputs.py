from typing import Annotated

import arrow
from arrow import Arrow
from pydantic import Field, BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict

ArrowFromAny = Annotated[Arrow, BeforeValidator(lambda v: arrow.get(v))]

class Inputs(BaseSettings):
    """Wrapper for the inputs provide to the report execution."""

    # Get the timestamp parsed out from ENV.
    # Timestamp contains a datetime (Arrow) instance which reflects when the report was originally executed the
    # first time. Retries will carry the same timestamp to make reports reproducible.
    timestamp: ArrowFromAny = Field(...)

    # Global settings config: prefix + nested delimiter
    model_config = SettingsConfigDict(
        env_prefix="LAKE_REPORTS__INPUTS__",
        env_nested_delimiter="__",
        extra="ignore",
        env_file=".env",  # optional
    )

def get_inputs() -> Inputs:
    # Reads from env (and .env if configured), applies validation & defaults
    return Inputs()