from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import fitz
import html

from app.detector.regex_detector import redact_text
from app.detector.nlp_detector import redact_entities


app = FastAPI(
    title="HealthTech PHI/PII Redaction Pipeline",
    version="1.0.0"
)


class TextRequest(BaseModel):
    text: str


# --------------------------------------------------
# Dashboard
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def dashboard():

    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>

        <title>HealthTech PHI/PII Protection</title>

        <meta name="viewport" content="width=device-width, initial-scale=1">

        <style>

            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f4f7fb;
                color: #1f2937;
            }

            .header {
                background: #0f172a;
                color: white;
                padding: 25px;
                text-align: center;
            }

            .header h1 {
                margin: 0;
                font-size: 28px;
            }

            .header p {
                margin-top: 8px;
                color: #cbd5e1;
            }

            .container {
                max-width: 1100px;
                margin: 35px auto;
                padding: 0 20px;
            }

            .card {
                background: white;
                padding: 25px;
                margin-bottom: 25px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            }

            textarea {
                width: 100%;
                height: 180px;
                padding: 15px;
                border: 1px solid #cbd5e1;
                border-radius: 10px;
                box-sizing: border-box;
                resize: vertical;
                font-size: 15px;
            }

            input[type="file"] {
                width: 100%;
                padding: 12px;
                border: 1px dashed #94a3b8;
                border-radius: 10px;
                box-sizing: border-box;
            }

            button {
                margin-top: 20px;
                width: 100%;
                padding: 14px;
                background: #2563eb;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 17px;
                cursor: pointer;
            }

            button:hover {
                background: #1d4ed8;
            }

            .or {
                text-align: center;
                margin: 20px 0;
                color: #64748b;
                font-weight: bold;
            }

            .features {
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
            }

            .feature {
                flex: 1;
                min-width: 180px;
                padding: 20px;
                background: #f8fafc;
                border-radius: 10px;
                text-align: center;
            }

            .feature strong {
                display: block;
                font-size: 18px;
                margin-bottom: 5px;
            }

            .footer {
                text-align: center;
                color: #64748b;
                padding: 20px;
            }

        </style>

    </head>

    <body>

        <div class="header">

            <h1>🏥 HealthTech PHI/PII Protection</h1>

            <p>
                Automated Healthcare Data Redaction & Pseudonymization
            </p>

        </div>


        <div class="container">

            <div class="card">

                <h2>🔐 Protect Patient Data</h2>

                <p>
                    Enter patient information or upload a PDF medical report.
                </p>


                <form action="/process" method="post" enctype="multipart/form-data">

                    <label>
                        <strong>Patient Text</strong>
                    </label>

                    <br><br>

                    <textarea
                        name="text"
                        placeholder="Example: Rahul Sharma visited Apollo Hospital in Delhi. Phone: 9876543210"
                    ></textarea>


                    <div class="or">
                        OR
                    </div>


                    <label>
                        <strong>Upload Medical PDF</strong>
                    </label>

                    <br><br>

                    <input
                        type="file"
                        name="pdf"
                        accept=".pdf"
                    >


                    <button type="submit">
                        🔒 Protect Patient Data
                    </button>

                </form>

            </div>


            <div class="card">

                <h2>⚙️ Detection Pipeline</h2>

                <div class="features">

                    <div class="feature">
                        <strong>Regex</strong>
                        Phone<br>
                        Email<br>
                        Date
                    </div>

                    <div class="feature">
                        <strong>spaCy NLP</strong>
                        Person<br>
                        Organization<br>
                        Location
                    </div>

                    <div class="feature">
                        <strong>Pseudonymization</strong>
                        PATIENT_001<br>
                        HOSPITAL_001<br>
                        LOCATION_001
                    </div>

                </div>

            </div>


            <div class="footer">
                HealthTech PHI/PII Redaction Pipeline • FastAPI
            </div>

        </div>

    </body>
    </html>
    """)


# --------------------------------------------------
# Process Text / PDF
# --------------------------------------------------

@app.post("/process", response_class=HTMLResponse)
async def process_report(
    text: str = Form(""),
    pdf: UploadFile = File(None)
):

    extracted_text = text

    # Process uploaded PDF
    if pdf is not None and pdf.filename:

        pdf_bytes = await pdf.read()

        document = fitz.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        extracted_text = ""

        for page in document:
            extracted_text += page.get_text()

        document.close()


    # Run detection pipeline
    regex_output = redact_text(extracted_text)

    final_output = redact_entities(regex_output)


    # Escape text before displaying it in HTML
    safe_original = html.escape(extracted_text)
    safe_redacted = html.escape(final_output)


    return HTMLResponse(
        content=f"""
        <!DOCTYPE html>

        <html>

        <head>

            <title>Redaction Result</title>

            <meta name="viewport"
                  content="width=device-width, initial-scale=1">

            <style>

                body {{
                    margin: 0;
                    font-family: Arial, sans-serif;
                    background: #f4f7fb;
                    color: #1f2937;
                }}

                .header {{
                    background: #0f172a;
                    color: white;
                    padding: 25px;
                    text-align: center;
                }}

                .container {{
                    max-width: 1200px;
                    margin: 35px auto;
                    padding: 0 20px;
                }}

                .grid {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 20px;
                }}

                .card {{
                    background: white;
                    padding: 25px;
                    border-radius: 15px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                }}

                .text {{
                    background: #f8fafc;
                    padding: 20px;
                    border-radius: 10px;
                    min-height: 220px;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }}

                .protected {{
                    border-left: 5px solid #16a34a;
                }}

                .status {{
                    padding: 15px;
                    background: #dcfce7;
                    color: #166534;
                    border-radius: 10px;
                    margin-bottom: 20px;
                    font-weight: bold;
                }}

                .button {{
                    display: inline-block;
                    margin-top: 25px;
                    padding: 12px 25px;
                    background: #2563eb;
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                }}

                @media(max-width: 800px) {{
                    .grid {{
                        grid-template-columns: 1fr;
                    }}
                }}

            </style>

        </head>


        <body>

            <div class="header">

                <h1>🏥 HealthTech PHI/PII Protection</h1>

                <p>Processing Result</p>

            </div>


            <div class="container">

                <div class="status">
                    ✅ Patient data processed successfully
                </div>


                <div class="grid">


                    <div class="card">

                        <h2>📄 Original Patient Data</h2>

                        <div class="text">
                            {safe_original}
                        </div>

                    </div>


                    <div class="card protected">

                        <h2>🔐 Protected Data</h2>

                        <div class="text">
                            {safe_redacted}
                        </div>

                    </div>


                </div>


                <div class="card" style="margin-top:20px;">

                    <h2>🛡️ Protection Pipeline</h2>

                    <p>✓ Regex-based PHI detection</p>

                    <p>✓ spaCy NLP entity detection</p>

                    <p>✓ Consistent entity pseudonymization</p>

                    <p>✓ Protected output generated</p>

                    <a class="button" href="/">
                        ← Process Another Report
                    </a>

                </div>

            </div>

        </body>

        </html>
        """
    )


# --------------------------------------------------
# REST API
# --------------------------------------------------

@app.post("/redact")
def redact(request: TextRequest):

    regex_output = redact_text(request.text)

    final_output = redact_entities(regex_output)

    return {
        "original_text": request.text,
        "redacted_text": final_output
    }