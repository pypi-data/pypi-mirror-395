import json
from pydantic_settings import BaseSettings
from pathlib import Path
from fastpage.app import APP_PATH
from importlib import import_module


class DefaultSettings(BaseSettings):
    app_name: str = "My App"


def load_settings() -> BaseSettings:
    app_name = APP_PATH.name
    config_module_name = "config"

    try:
        config_module = import_module(config_module_name)
    except ModuleNotFoundError:
        config_module = None

    if config_module:
        settings = config_module.Settings()
    else:
        settings = DefaultSettings()

    config_path = Path.home() / f".{app_name}" / "config.json"
    settings_data = {}

    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, "w") as f:
            json.dump(settings.model_dump(), f, indent=4)
    else:
        with open(config_path, "r") as f:
            settings_data = json.load(f)

    return settings.model_validate(settings_data)

def update_settings(key, value) -> BaseSettings:
    app_name = APP_PATH.name
    config_path = Path.home() / f".{app_name}" / "config.json"

    settings = load_settings()

    setattr(settings, key, value)

    with open(config_path, "w") as f:
        json.dump(settings.model_dump(), f, indent=4)


settings = load_settings()