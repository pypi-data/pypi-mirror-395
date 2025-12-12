from googletrans import Translator


_translator = Translator()


def translate(text: str, dst_lng: str) -> str:
    """Translate a given text string into the specified target language.

    This function uses the `googletrans` library (Google Translate API wrapper)
    to translate text from its detected source language into a destination
    language code such as `"pl"`, `"en"`, `"de"`, etc.

    Args:
        text (str): The input text to translate.
        dst_lng (str): The target language code (ISO 639-1), e.g. "pl" for Polish.

    Returns:
        str: The translated text.

    Notes:
        - Surrounding whitespace is stripped before sending to the translator.
        - Language detection is handled automatically by googletrans.
        - Network connectivity is required since translations use Google's API.
    """
    translated = _translator.translate(text.strip(), dest=dst_lng).text
    return translated