import re
from collections import defaultdict

def pre_tokenize(text: str, lowercase: bool = True) -> list:
    """
    Pre-tokenizes the input text by splitting on whitespace and punctuation.

    Args:
        text (str): The input text to be pre-tokenized.

    Returns:
        List[str]: A list of pre-tokenized words.
    """
    if lowercase:
        text = text.lower()
    tokens = re.findall(r'\w+|[^\w\s]', text, re.UNICODE)
    return tokens




def normalize_text(text: str, lowercase: bool = True) -> str:
    """
    Normalizes the input text by removing extra spaces.

    Args:
        text (str): The input text to be normalized.

    Returns:
        str: The normalized text.
    """
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower() if lowercase else text



if __name__ == "__main__":
    sample_text = "Hello, world! This is a test."
    print("Pre-tokenized:", pre_tokenize(sample_text))
    print("Vocabulary:", initialize_vocab(sample_text))