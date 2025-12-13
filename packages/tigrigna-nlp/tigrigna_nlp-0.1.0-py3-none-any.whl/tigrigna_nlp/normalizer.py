# tigrigna_nlp/normalizer.py
def normalize(text: str) -> str:
    """Standard Tigrinya/Amharic character normalization"""
    mapping = {
        "ሃ":"ሀ", "ሓ":"ሀ", "ኅ":"ሀ", "ሐ":"ሀ", "ኃ":"ሀ", "ኻ":"ኃ",
        "ሑ":"ሁ", "ሒ":"ሂ", "ኁ":"ሁ", "ኂ":"ሂ",
        "ሕ":"ህ", "ኅ":"ህ", "ሖ":"ሆ", "ኆ":"ሆ",
        "ሠ":"ሰ", "ሡ":"ሱ", "ሢ":"ሲ", "ሣ":"ሳ", "ሤ":"ሴ", "ሥ":"ስ", "ሦ":"ሶ",
        "ዉ":"ው", "ዎ":"ወ", "ዐ":"አ", "ዑ":"ኡ", "ዒ":"ኢ", "ዓ":"አ", "ዔ":"ኤ", "ዕ":"እ", "ዖ":"ኦ"
    }
    for k, v in mapping.items():
        text = text.replace(k, v)
    return text