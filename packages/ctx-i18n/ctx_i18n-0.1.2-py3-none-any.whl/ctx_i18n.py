from pathlib import Path
from functools import lru_cache
import os
from typing import Optional, Dict, Any
from contextvars import ContextVar
import yaml
from jq_utils import jq_get

# Internal context variables for the i18n library
locale: ContextVar[str] = ContextVar("locale", default="en")
translations: ContextVar[Dict[str, Any]] = ContextVar("translations", default={})

@lru_cache(maxsize=None)
def load_translations(locale_str: str, base_path: Optional[Path] = None):
    """
    Loads the translation file for a given locale.
    The result is cached to avoid reading the file on every request.
    """
    if base_path is None:
        app_path_env = os.getenv("APP_PATH")
        if app_path_env:
            base_path = Path(app_path_env)
        else:
            base_path = Path(".") # Current directory as a last resort

    locales_dir = base_path / "locales"
    path = locales_dir / f"{locale_str}.yml"

    if not path.exists():
        # Fallback to English if the locale file doesn't exist
        path = locales_dir / "en.yml"
        if not path.exists():
            # If even en.yml doesn't exist, raise an error or return empty
            # For now, let's raise an error as it indicates a setup issue
            raise FileNotFoundError(f"Translation file for 'en' not found at {path}")

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def set_locale(locale_str: str, base_path: Optional[Path] = None):
    """
    Sets the locale and loads the corresponding translations into the context.
    """
    locale.set(locale_str)
    loaded_translations = load_translations(locale_str, base_path=base_path)
    translations.set(loaded_translations)

def _(key: str, **kwargs) -> str:
    """
    Gets a translation string by key from the registered context.
    """
    translation = jq_get(translations.get(), key)
    if translation is None:
        return key
    return translation.format(**kwargs)
