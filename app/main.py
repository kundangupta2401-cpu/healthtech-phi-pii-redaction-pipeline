from fastapi import FastAPI

app = FastAPI(
    title="HealthTech PHI/PII Redaction Pipeline",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "status": "running",
        "message": "HealthTech PHI/PII Redaction Pipeline"
    }