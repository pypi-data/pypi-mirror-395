import gettext
from pathlib import Path

GETTEXT_DOMAIN = 'autoland'

locale_dir = Path(__file__).parent / "locales"

translation = gettext.translation(
    GETTEXT_DOMAIN,
    localedir=str(locale_dir),
    fallback=True
)

_ = translation.gettext
