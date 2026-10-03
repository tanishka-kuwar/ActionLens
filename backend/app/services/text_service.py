import re


def clean_text(text: str) -> str:
    """
    Clean extracted document text.

    Operations:
    1. Remove extra spaces
    2. Normalize line breaks
    3. Remove unnecessary blank lines
    4. Remove spaces at the beginning/end of lines
    """

    # Replace Windows-style line endings with standard line endings
    text = text.replace("\r\n", "\n")

    # Remove leading and trailing spaces from every line
    lines = [line.strip() for line in text.split("\n")]

    # Remove completely empty lines
    lines = [line for line in lines if line]

    # Join lines into a clean readable text
    cleaned_text = "\n".join(lines)

    # Replace multiple spaces with a single space
    cleaned_text = re.sub(r"[ \t]+", " ", cleaned_text)

    return cleaned_text.strip()