import json
import os
from typing import Any


def get_layout(extract_folder: str) -> dict[str, Any]:
    """Loads and returns the Power BI Layout JSON from an extracted PBIX folder.

    The Layout file defines report pages, visuals, textbox content,
    and metadata. It is stored UTF-16LE encoded inside:

        <extract_folder>/Report/Layout

    Args:
        extract_folder (str): Path to the folder containing the extracted PBIX.

    Returns:
        dict[str, Any]: Parsed JSON object representing the report layout.

    Raises:
        FileNotFoundError: If the Layout file does not exist.
        JSONDecodeError: If the Layout file is not valid JSON.
    """
    layout_path = os.path.join(extract_folder, "Report/Layout")
    with open(layout_path, 'r', encoding='utf-16le') as f:
        layout = json.load(f)
    return layout


def save_layout(layout: dict[str, Any], extract_folder: str) -> dict[str, Any]:
    """Saves the modified layout JSON back to the extracted PBIX folder.

    The Layout file must be saved using UTF-16LE encoding,
    otherwise Power BI Desktop will refuse to load the PBIX.

    Args:
        layout (dict[str, Any]): Updated layout JSON object.
        extract_folder (str): Path to the extracted PBIX folder.

    Returns:
        dict[str, Any]: The same layout object (returned for convenience).

    Raises:
        FileNotFoundError: If the target directory does not exist.
    """
    layout_path = os.path.join(extract_folder, "Report/Layout")
    json_str = json.dumps(layout, ensure_ascii=False, separators=(',', ':'))
    with open(layout_path, 'w', encoding='utf-16le') as f:
        f.write(json_str)
    return layout