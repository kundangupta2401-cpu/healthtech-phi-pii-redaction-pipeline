from app.detector.pseudonymizer import Pseudonymizer
import spacy

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# Create one pseudonymizer object
pseudonymizer = Pseudonymizer()


def redact_entities(text: str) -> str:
    """
    Detect and pseudonymize named entities using spaCy.
    """

    doc = nlp(text)

    redacted_text = text

    # Process entities from end to beginning
    for entity in reversed(doc.ents):

        if entity.label_ == "PERSON":
            replacement = pseudonymizer.get_pseudonym(entity.text, "PERSON")

        elif entity.label_ == "ORG":
            replacement = pseudonymizer.get_pseudonym(entity.text, "ORG")

        elif entity.label_ == "GPE":
            replacement = pseudonymizer.get_pseudonym(entity.text, "GPE")

        else:
            continue

        redacted_text = (
            redacted_text[:entity.start_char]
            + replacement
            + redacted_text[entity.end_char:]
        )

    return redacted_text


if __name__ == "__main__":

    sample = "Rahul Sharma visited Apollo Hospital in Delhi. Rahul Sharma came back."

    print(redact_entities(sample))