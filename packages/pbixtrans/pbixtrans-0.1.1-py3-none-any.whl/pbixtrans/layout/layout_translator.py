import json
from typing import Any

from pbixtrans.layout.section import translate_section
from pbixtrans.layout.registry import VISUAL_TRANSLATORS


def translate_layout(layout: dict[str, Any], dst_lng: str) -> dict[str, Any]:
    """Translate all text content inside a textbox visual in place.

    Each visual translator is dispatched dynamically based on visual type
    using the `VISUAL_TRANSLATORS` registry. All modifications are applied
    in place to the input layout dictionary.

    Args:
        layout (dict[str, Any]): The parsed Power BI layout JSON object.
        dst_lng (str): Target language code (ISO 639-1), e.g. "pl" for Polish.

    Returns:
        dict[str, Any]: The modified layout object with translated text.
    """
    print(f"Translating to '{dst_lng}'")

    for section in layout.get('sections', []):
        translate_section(section, dst_lng)

        for vc in section.get('visualContainers', []):
            config = vc["config"]
            vc_config = json.loads(config) if isinstance(config, str) else config
            single = vc_config.get("singleVisual", {})
            vtype = single.get("visualType")

            handler = VISUAL_TRANSLATORS.get(vtype)
            if handler:
                handler(single, dst_lng)

            vc['config'] = json.dumps(vc_config, ensure_ascii=False, separators=(',', ':'))
            
    return layout
