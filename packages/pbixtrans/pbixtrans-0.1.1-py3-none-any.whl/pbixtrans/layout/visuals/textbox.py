from typing import Any

from pbixtrans.translator import translate


def translate_textbox(single_visual: dict[str, Any], dst_lng: str) -> None:
    """Translate all text content inside a textbox visual in place.

    The dictionary is modified directly, so no value is returned.

    Args:
        single_visual (dict): The "singleVisual" configuration object for a
            textbox visual, containing its objects and text content.
        dst_lng (str): Target language code (ISO 639-1), e.g. "pl" for Polish.
    """
    for gen_object in single_visual.get('objects', {}).get('general', []):
        paragraphs = gen_object.get('properties', {}).get('paragraphs', [])
        for paragraph in paragraphs:
            for text_run in paragraph.get("textRuns", []):
                val = text_run.get("value", "")
                if isinstance(val, str) and val.strip():
                    translated_val = translate(val, dst_lng)
                    print(f"Textbox: '{val}' -> '{translated_val}'")
                    text_run["value"] = translated_val