# 🔐 HealthTech PHI/PII Redaction Pipeline

A privacy-focused healthcare data protection pipeline that detects sensitive patient information and transforms it into safe, pseudonymized/redacted data before it can be passed to downstream AI/LLM systems.

---

## 📌 Problem Statement

Healthcare applications increasingly use AI and Large Language Models (LLMs) for clinical documentation, summarization, and analysis.

However, healthcare records contain sensitive information such as:

- Patient names
- Phone numbers
- Email addresses
- Dates
- Hospital names
- Locations
- Other personally identifiable information

Sending this information directly to external AI services can create privacy and security risks.

### The Problem

> How can we protect sensitive patient information while preserving enough clinical context for AI systems to still understand the data?

---

## 💡 Our Solution

We developed a **hybrid PHI/PII protection pipeline** that works as a privacy layer between healthcare data and downstream AI/LLM systems.

The system combines:

- Regex-based detection
- NLP-based entity detection
- Pseudonymization
- PDF text extraction
- FastAPI backend
- Web-based dashboard

### Core Pipeline

```text
Patient Data
     │
     ▼
Text / PDF Input
     │
     ▼
PDF Text Extraction
     │
     ▼
Regex Detection
     │
     ▼
spaCy NLP Detection
     │
     ▼
Pseudonymization / Redaction
     │
     ▼
Protected Patient Data
     │
     ▼
Downstream AI / LLM