import spacy

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")


def redact_entities(text: str) -> str:
    """
    Detect and redact named entities using spaCy.
    """

    doc = nlp(text)

    redacted_text = text

    for entity in reversed(doc.ents):

        if entity.label_ == "PERSON":
            replacement = "[PERSON]"

        elif entity.label_ == "ORG":
            replacement = "[ORGANIZATION]"

        elif entity.label_ == "GPE":
            replacement = "[LOCATION]"

        else:
            continue

        redacted_text = (
            redacted_text[:entity.start_char]
            + replacement
            + redacted_text[entity.end_char:]
        )

    return redacted_text

