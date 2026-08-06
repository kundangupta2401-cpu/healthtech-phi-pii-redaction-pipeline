from fastapi import FastAPI
from httpcore import request
from pydantic import BaseModel

from app.detector.regex_detector import redact_text
from app.detector.nlp_detector import redact_entities

app = FastAPI(
    title="HealthTech PHI/PII Redaction Pipeline",
    version="1.0.0"
)


class TextRequest(BaseModel):
    text: str


@app.get("/")
def home():
    return {
        "status": "running",
        "message": "HealthTech PHI/PII Redaction Pipeline"
    }


@app.post("/redact")
def redact(request: TextRequest):

    regex_output = redact_text(request.text)

    final_output = redact_entities(regex_output)

    return {
        "original_text": request.text,
        "redacted_text": final_output
    }