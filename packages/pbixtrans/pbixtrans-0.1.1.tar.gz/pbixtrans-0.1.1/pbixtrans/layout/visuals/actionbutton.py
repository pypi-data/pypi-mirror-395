from typing import Any

from pbixtrans.translator import translate


def translate_actionbutton(single_visual: dict[str, Any], dst_lng: str) -> None:
    """Translate all text content inside an action button visual in place.

    The dictionary is modified directly, so no value is returned.

    Args:
        single_visual (dict): The "singleVisual" configuration object for a
            action button visual, containing its objects and text content.
        dst_lng (str): Target language code (ISO 639-1), e.g. "pl" for Polish.
    """
    for text_obj in single_visual.get('objects', {}).get('text', []):
        properties = (
            text_obj
            .get('properties', {})
            .get('text', {})
            .get('expr', {})
            .get('Literal', {})
        )
        val = properties.get("Value", "")
        if isinstance(val, str) and val.strip() and val.strip("'"):
            translated_val = "'" + translate(val.strip("'"), dst_lng) + "'"
            print(f"Action Button: '{val}' -> '{translated_val}'")
            properties["Value"] = translated_val