"""Internationalization module for streamlit-app-generator."""
import os
import locale
from typing import Dict, Any


class I18n:
    """Internationalization handler."""

    def __init__(self, language: str = None):
        """Initialize i18n with language."""
        self.language = language or self._detect_language()
        self.translations = self._load_translations()

    def _detect_language(self) -> str:
        """Detect system language."""
        try:
            # Try to get system language
            system_lang = locale.getdefaultlocale()[0]
            if system_lang:
                if system_lang.startswith('pt'):
                    return 'pt-BR'
                return 'en'
        except:
            pass
        return 'en'

    def _load_translations(self) -> Dict[str, Any]:
        """Load translations for current language."""
        from . import translations_en, translations_pt_br

        translations_map = {
            'en': translations_en.TRANSLATIONS,
            'pt-BR': translations_pt_br.TRANSLATIONS,
            'pt': translations_pt_br.TRANSLATIONS,
        }

        return translations_map.get(self.language, translations_en.TRANSLATIONS)

    def t(self, key: str, **kwargs) -> str:
        """Translate a key with optional formatting."""
        # Navigate nested keys (e.g., "wizard.welcome.title")
        keys = key.split('.')
        value = self.translations

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, key)
            else:
                return key

        # Format with kwargs if provided
        if kwargs and isinstance(value, str):
            try:
                return value.format(**kwargs)
            except KeyError:
                return value

        return value if isinstance(value, str) else key

    def get_language_name(self) -> str:
        """Get the full name of current language."""
        names = {
            'en': 'English',
            'pt-BR': 'Português (Brasil)',
            'pt': 'Português (Brasil)',
        }
        return names.get(self.language, 'English')


# Global i18n instance
_i18n_instance = None


def get_i18n(language: str = None) -> I18n:
    """Get or create i18n instance."""
    global _i18n_instance
    if _i18n_instance is None or language is not None:
        _i18n_instance = I18n(language)
    return _i18n_instance


def t(key: str, **kwargs) -> str:
    """Shorthand for translation."""
    return get_i18n().t(key, **kwargs)
