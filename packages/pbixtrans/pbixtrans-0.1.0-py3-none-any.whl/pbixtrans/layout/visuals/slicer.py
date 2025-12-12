from typing import Any

from pbixtrans.translator import translate


def translate_slicer(single_visual: dict[str, Any], dst_lng: str) -> None:
    """Translate all text content inside a slicer visual in place.

    The dictionary is modified directly, so no value is returned.

    Args:
        single_visual (dict): The "singleVisual" configuration object for a
            slicer visual, containing its objects and text content.
        dst_lng (str): Target language code (ISO 639-1), e.g. "pl" for Polish.
    """
    col_prop = single_visual.get("columnProperties", {})
    if col_prop:
        for table_col, col_name_dict in col_prop.items():
            val = col_name_dict.get("displayName", "")
            if isinstance(val, str) and val.strip():
                translated_val = translate(val, dst_lng)
                print(f"Slicer: '{val}' -> '{translated_val}'")
                col_name_dict["displayName"] = translated_val
    else:
        dict_ = {}
        for item in single_visual.get("prototypeQuery", {}).get("Select", []):
            table_col = item.get("Name", "")
            val = item.get("Column", {}).get("Property", "")
            translated_val = translate(val, dst_lng)
            print(f"Slicer: '{val}' -> '{translated_val}'")
            dict_[table_col] = {"displayName": translated_val}
        single_visual['columnProperties'] = dict_