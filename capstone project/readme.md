# Cred Domain Support Agent (CrewAI Enterprise System)

This repository implements an air-gapped, production-grade **Cred (Banking & FinTech)** Domain Support Agent featuring a dual-chunking local RAG core, real-time multi-factor risk escalation, strict token cost caps, input-side PII masking, automated compliance review loops, and an interactive Streamlit Chat User Interface (`ui.py`).

---

## 📊 1. Seeded Dataset & Verification Parameters

Synthetic dataset generation parameters within `dataset.py` are structurally fixed for test reproducibility:
* **Randomization Seed:** `42`
* **Category Coverage:** Multi-tenant representation across `Personal Loan`, `Home Loan`, `Auto Loan`, `Education Loan`, and `Business Loan` ($\ge 3$ records per category).
* **Lifecycle State Coverage:** States include `Submitted`, `Under Review`, `Approved`, `Rejected`, and `Disbursed` ($\ge 1$ record per status).
* **Loan Amount Scale:** Tiered distribution spanning **50,000 INR to 5,000,000 INR**.
* **Target Fraud Ratio Achieved:** **16.28%** (satisfying the 10%–30% pipeline constraint programmatically).

---

## 🧠 2. Groundedness RAG Calibration & Fallback

* **Empirical Fallback Threshold:** Calibrated at **`0.12`** based on similarity score mapping.
* **Punctuation & Stopword Normalization:** Strips trailing punctuation (`?`, `!`, `.`) and processes keyword matching filters in `rag_core.py`.
* **Groundedness Action Fired:** Out-of-scope queries trigger the safe fallback: *"I am sorry, but the retrieved context does not provide sufficient information to safely answer this question."*

---

## 💻 3. Interactive Streamlit UI Architecture (`ui.py`)

* **Dynamic Multi-Tenant Controls:** Features a sidebar **Target Loan Record ID** input window querying the active database dynamically.
* **UI-Layer Checkpoints:** Blocks empty text submissions and validates profile strings (e.g., `CRED-LN-1001`).
* **Error Resilience:** Translates backend HTTP states (`404 Record Not Found`, `400 Budget Exceeded`, `500 Internal Crash`) into user-facing status alerts.

---

## 🏃‍♂️ 4. Step-by-Step System Execution Guide

### Step 4.1: Sandbox Environment Setup
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
pip install fastapi uvicorn pydantic crewai pyautogen websockets requests numpy python-dotenv streamlit
```

### Step 4.2: Enforce Zero-Network Air-Gapped Controls
Add these flags to your local `.env` configuration file:
```env
CREWAI_DISABLE_TELEMETRY=true
OTEL_SDK_DISABLED=true
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### Step 4.3: Boot the FastAPI Server (Terminal 1)
```bash
python -m uvicorn app:app --host 127.0.0.1 --port 8090
```
*Verification:* Confirm `INFO: Uvicorn running on http://127.0.0.1:8090`.

### Step 4.4: Launch the Streamlit User Interface (Terminal 2)
```bash
streamlit run ui.py
```
*Action:* Opens the interactive UI dashboard at **`http://localhost:8501`**.

---

## 🧪 5. Verification & Testing Matrix

1. **Run the 15-Query Evaluation Suite (Automated Grade Test):**
   ```bash
   python evaluate_agent.py
   ```
   *Expected Output:* Reports a **1.00 score average** for Accuracy, Grounding, Completeness, and Safety across mandatory banking topics.
2. **Live UI Policy Testing (`http://localhost:8501`):** Enter `CRED-LN-1001` in the sidebar and query policy guidelines.
3. **PII Masking and Log Validation:** Verify raw PAN strings are masked as `[MASKED_PAN]` in server terminal logs.
