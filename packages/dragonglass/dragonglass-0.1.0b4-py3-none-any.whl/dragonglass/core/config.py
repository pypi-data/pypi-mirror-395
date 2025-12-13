from pathlib import Path
from typing import Literal, Type, Tuple, List

from pydantic import Field, BaseModel, AliasChoices
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
    TomlConfigSettingsSource,
)
from platformdirs import user_config_dir, user_data_dir, user_cache_dir

APP_NAME = "dg"
CONFIG_FILE_NAME = "config.toml"


class GeminiSettings(BaseModel):
    """Settings for the Gemini API."""

    api_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices("google_api_key", "GOOGLE_API_KEY", "api_key")
    )
    default_model: str = "gemini-3-pro-preview"
    temperature: float = Field(0.7, ge=0.0, le=1.0)
    max_tokens: int | None = Field(None, ge=1)
    top_p: float = Field(1.0, ge=0.0, le=1.0)

    # Safety settings - support both keys for backward compatibility
    safety_settings: Literal["BLOCK_NONE", "HARM_ONLY"] = Field(
        "BLOCK_NONE",
        validation_alias=AliasChoices("safety_settings", "safe_settings")
    )

    # Grounding for Google Search
    grounding_enabled: bool = False


class AppSettings(BaseSettings):
    """Main application settings."""
    
    # XDG Base Directory Specification paths
    config_dir: Path = Field(default_factory=lambda: Path(user_config_dir(APP_NAME)))
    data_dir: Path = Field(default_factory=lambda: Path(user_data_dir(APP_NAME)))
    cache_dir: Path = Field(default_factory=lambda: Path(user_cache_dir(APP_NAME)))

    # Nested settings for Gemini
    gemini: GeminiSettings

    model_config = SettingsConfigDict(
        extra="ignore",
        env_prefix="DG_",
        env_nested_delimiter="__",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        """
        Customizes the order of setting sources.
        Priority: Init > Env > Local Config (CWD) > User Config (XDG) > DotEnv > Secrets
        """
        
        # Potential config file locations
        cwd_config = Path.cwd() / CONFIG_FILE_NAME
        user_config = Path(user_config_dir(APP_NAME)) / CONFIG_FILE_NAME
        
        # We want to load from multiple TOML files if they exist.
        # The earlier in the list, the higher the priority.
        toml_sources: List[PydanticBaseSettingsSource] = []
        
        # 1. CWD config (highest priority among files)
        if cwd_config.is_file():
            toml_sources.append(TomlConfigSettingsSource(settings_cls, toml_file=cwd_config))
            
        # 2. User config (XDG)
        if user_config.is_file():
            toml_sources.append(TomlConfigSettingsSource(settings_cls, toml_file=user_config))

        return (
            init_settings,
            env_settings,
            *toml_sources,
            dotenv_settings,
            file_secret_settings,
        )

    def ensure_dirs(self):
        """Ensures that XDG directories exist."""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            self.data_dir.mkdir(parents=True, exist_ok=True)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            # Log warning but don't crash immediately? 
            # Actually, if data_dir fails, the DB will fail.
            # We'll re-raise for now as it's critical.
            raise RuntimeError(f"Failed to create application directories: {e}") from e


# Global settings instance
# This instantiates the settings, loading from all sources.
settings = AppSettings()

# Ensure directories exist on import (Side effect, but required for DB init in other modules)
settings.ensure_dirs()
