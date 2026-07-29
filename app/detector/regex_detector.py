import re

EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

PHONE_PATTERN = r'\b(?:\+91[-\s]?)?[6-9]\d{9}\b'

DATE_PATTERN = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'


def redact_text(text: str) -> str:
    """
    Replace sensitive information with placeholder tokens.
    """

    text = re.sub(EMAIL_PATTERN, "[EMAIL]", text)

    text = re.sub(PHONE_PATTERN, "[PHONE]", text)

    text = re.sub(DATE_PATTERN, "[DATE]", text)

    return text

import re

EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

PHONE_PATTERN = r'\b(?:\+91[-\s]?)?[6-9]\d{9}\b'

DATE_PATTERN = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'


def redact_text(text: str) -> str:
    """
    Replace sensitive information with placeholder tokens.
    """

    text = re.sub(EMAIL_PATTERN, "[EMAIL]", text)

    text = re.sub(PHONE_PATTERN, "[PHONE]", text)

    text = re.sub(DATE_PATTERN, "[DATE]", text)

    return text

