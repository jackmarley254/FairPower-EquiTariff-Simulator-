# ⚡ FairPower: EquiTariff Simulator (Backend API)

**Optimal Tariff Design for Energy Affordability & Equity**

This repository houses the Backend API for **FairPower**, an interactive simulator built for the **EPRA Hackathon 2026**. FairPower transitions Kenya's residential electricity tariff design from simple consumption bands (DC1, DC2, DC3) to a multi-variable, machine learning-driven clustering model.

---

## 🎯 The Problem
The current tariff structure suffers from misclassification and "cliff effects." A household consuming 30 kWh pays KES 12.22/kWh, but at 31 kWh, the rate jumps to KES 16.30/kWh—a 33% increase for a single unit. Relying solely on consumption ignores household size, poverty levels, and appliance ownership, leading to inequitable energy burdens.

## 💡 Our Solution
FairPower uses Machine Learning (K-Means/GMM) to segment households into four equitable clusters (Segments A-D) based on features like household size, county poverty index, and appliance ownership. 

This FastAPI backend serves as the core calculation engine, providing real-time bill simulation, pass-through charge locking (at March 2026 rates), and affordability metrics (like the 10% energy burden threshold) to our Streamlit frontend dashboard.

## 🛠️ Tech Stack
* **Framework:** FastAPI, Uvicorn
* **Data Validation:** Pydantic
* **Data & ML Loading:** Pandas, Scikit-learn, Joblib
* **Language:** Python 3.10+

## 🚀 Local Setup & Installation

**1. Clone the repository**
```bash
git clone [https://github.com/jackmarley254/FairPower-EquiTariff-Simulator-.git](https://github.com/jackmarley254/FairPower-EquiTariff-Simulator-.git)
cd FairPower-EquiTariff-Simulator-
2. Create and activate a virtual environment

Bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
3. Install dependencies

Bash
pip install -r requirements.txt
4. Run the development server

Bash
uvicorn backend.main:app --reload
5. View the Interactive API Docs
Navigate to http://127.0.0.1:8000/docs in your browser to test the endpoints via the auto-generated Swagger UI.

🔌 Core API Endpoints
GET /health - System health check.

POST /calculate-tariff - Accepts household features and a proposed tariff configuration, returning a detailed breakdown comparing the EPRA baseline bill against the proposed segment-based bill.

POST /simulate-scenario - (WIP) Batch simulation for revenue reconciliation.

GET /segments - (WIP) Fetches segment definitions and characteristics.

GET /metrics/affordability - (WIP) Fetches aggregated metrics like the Gini coefficient.

👥 The Team
Michael Chege Nganga: System Architect & Team Lead

Joel: Data Engineer (ML Layer)

Jackson: Backend Developer (API & Tariff Logic)

Ndirangu Juliet: Policy Lead & Frontend Developer

Built with ❤️ for equitable energy access in Kenya.


### Step 2: Commit and Push
Since this directly addresses the documentation issue, you can commit it to your feature branch using the magic words to close out the issue once it's merged into `dev`:

```bash
git add README.md
git commit -m "docs: write comprehensive README for local setup and API overview (closes #4)"
git push origin feature/backend