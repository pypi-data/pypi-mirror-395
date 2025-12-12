from typing import Any

from pbixtrans.translator import translate


def translate_section(section: dict[str, Any], dst_lng: str) -> None:
    """Translate the display name of a layout section (page) in place.

    The dictionary is modified directly, so no value is returned.

    Args:
        section (dict): A section object from the PBIX layout, typically
            containing a "displayName" key.
        dst_lng (str): Target language code (ISO 639-1), e.g. "pl" for Polish.
    """
    if 'displayName' in section:
        original = section['displayName']
        translated = translate(original, dst_lng)
        section['displayName'] = translated
        print(f"Section: '{original}' -> '{translated}'")
