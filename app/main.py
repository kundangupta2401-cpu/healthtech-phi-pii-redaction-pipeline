from fastapi import FastAPI
from pydantic import BaseModel

from app.detector.regex_detector import redact_text

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

    redacted_output = redact_text(request.text)

    return {
        "original_text": request.text,
        "redacted_text": redacted_output
    }