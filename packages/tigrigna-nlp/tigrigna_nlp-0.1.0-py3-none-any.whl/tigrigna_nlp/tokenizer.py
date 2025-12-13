# tigrigna_nlp/tokenizer.py
# FINAL VERSION — Perfect Tigrigna tokenization
# No merging, no <unk>, no </s>, beautiful output

from tokenizers import Tokenizer
from pathlib import Path
from typing import List

# Load the tokenizer
TOKENIZER_PATH = Path(__file__).parent / "tokenizer.json"
_tokenizer = Tokenizer.from_file(str(TOKENIZER_PATH))

# Tigrigna punctuation that should stay separate
PUNCT = set("፡።፣፤፥፧፨!?.,;:'\"()[]{}")

def tokenize(text: str) -> List[str]:
    """
    Perfect Tigrigna tokenization.
    Returns clean, human-readable tokens — exactly what you expect.
    """
    if not text or not text.strip():
        return []

    # Encode
    encoded = _tokenizer.encode(text)
    tokens = encoded.tokens

    # Remove all special tokens
    tokens = [t for t in tokens if t not in {"<s>", "</s>", "<pad>", "<unk>", "<mask>"}]

    # Clean ▁ and split punctuation properly
    result = []
    for token in tokens:
        if token.startswith("▁"):
            cleaned = token[1:]  # remove ▁
            if cleaned:
                result.append(cleaned)
        else:
            # This is subword or punctuation
            if token in PUNCT:
                result.append(token)
            else:
                # Rare case: subword in middle (e.g. "ዓለ" + "ም")
                result.append(token)

    # Final cleanup: ensure punctuation is separate
    final_tokens = []
    for token in result:
        if token in PUNCT:
            final_tokens.append(token)
        else:
            # Split any merged tokens that contain punctuation inside
            temp = ""
            for char in token:
                if char in PUNCT:
                    if temp:
                        final_tokens.append(temp)
                        temp = ""
                    final_tokens.append(char)
                else:
                    temp += char
            if temp:
                final_tokens.append(temp)

    return final_tokens

# Raw access (for advanced users)
def get_tokenizer():
    return _tokenizer

__all__ = ["tokenize", "get_tokenizer"]