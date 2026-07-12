# MSME Financial Health Assessment
> AI-powered MSME Credit Risk Assessment & Financial Health Analytics Platform

This project is an end-to-end machine learning platform that predicts the Probability of Default (PD) for Micro, Small, and Medium Enterprises (MSMEs) and converts it into an interpretable Financial Health Score with actionable recommendations.

## 🚀 Live Demo
🔗 Dashboard: deployment link will be updated soon.  

---

## Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Machine Learning Pipeline](#machine-learning-pipeline)
- [Model Validation](#model-validation)
- [Financial Health Score Methodology](#financial-health-score-methodology)
- [API Documentation](#api-documentation)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)

---

## Features
### Individual Business Assessment
- Predict Probability of Default (PD)
- Financial Health Score (0–100)
- Credit Risk Score
- Credit Grade (AAA, AA, A, BBB, High Risk)
- Loan Readiness Assessment
- Dimension-wise Health Scores
- AI-generated Risk Explanation
- Personalized Improvement Recommendations

### Portfolio Analytics
Upload a CSV containing multiple MSMEs and instantly obtain:
- Portfolio Summary
- Average Financial Health
- Average Probability of Default
- Average Credit Risk Score
- Grade Distribution
- High Risk Business List
- Portfolio Statistics
- Risk Distribution Charts
- Interactive Business Selection

---

## Technology Stack

### Machine Learning
- Python
- Scikit-Learn
- XGBoost
- SHAP
- Pandas
- NumPy

### Backend
- FastAPI
- Pydantic
- Uvicorn

### Frontend
- Streamlit
- Plotly

### Model Serialization
- Joblib


---

## System Architecture

```text
                    ┌─────────────────────┐
                    │        User         │
                    │  MSME Analyst /     │
                    │  Financial Officer  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Frontend        │
                    │ Streamlit Dashboard │
                    │                     │
                    │ - Customer          │
                    │   Assessment        │
                    │ - Portfolio         │
                    │   Analytics         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Backend        │
                    │      FastAPI        │
                    │                     │
                    │ - API Routes        │
                    │ - Request Handling  │
                    │ - Business Logic    │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │       Machine Learning Layer   │
              │                                │
              │ - XGBoost PD Prediction Model  │
              │ - Probability Calibration      │
              │ - SHAP Explainability          │
              │ - Financial Health Scoring     │
              └───────────────┬────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │       Output        │
                    │                     │
                    │ - Default Risk      │
                    │   Probability (PD)  │
                    │ - Health Score      │
                    │ - Risk Explanation  │
                    │ - Recommendations   │
                    └─────────────────────┘

```

---

## Project Structure
```
msme-financial-health-assessment/
│
├── backend/          # FastAPI backend and API services
├── frontend/         # Streamlit dashboard interface
├── models/           # Trained ML models and artifacts
├── notebooks/        # ML experiments and analysis
├── src/              # Core ML pipeline code
├── data/             # Training, testing and sample portfolio datasets
├── data_generation/  # Synthetic MSME data generation
├── docs/             # Documentation and data dictionary
└── README.md
```

## Machine Learning Pipeline
This project follows an end-to-end machine learning pipeline that processes MSME financial data to predict credit risk, provide explanations, and generate a Financial Health Score.

```text
                  MSME Dataset
                       │
                       ▼
          ┌────────────────────────┐
          │ Data Processing Layer  │
          │                        │
          │ - Data Loading         │
          │ - Data Inspection      │
          │ - Data Quality Report  │
          │ - Target Leakage Check │
          │ - Train/Test Split     │
          └───────────┬────────────┘
                      │
                      ▼
          ┌────────────────────────┐
          │ Preprocessing Pipeline │
          │                        │
          │ - Missing Value        │
          │   Handling             │
          │ - Categorical Encoding │
          │ - Numerical Processing │
          │ - Feature Preparation  │
          └───────────┬────────────┘
                      │
                      ▼
          ┌────────────────────────┐
          │ Model Training         │
          │                        │
          │ XGBoost Classifier     │
          │                        │
          │ - Class Imbalance      │
          │   Handling             │
          │ - Pipeline Training    │
          │ - Model Serialization  │
          └───────────┬────────────┘
                      │
                      ▼
          ┌────────────────────────┐
          │ Model Evaluation       │
          │                        │
          │ - Accuracy             │
          │ - Precision            │
          │ - Recall               │
          │ - F1 Score             │
          │ - ROC-AUC              │
          │ - ROC / PR Curves      │
          └───────────┬────────────┘
                      │
                      ▼
          ┌────────────────────────┐
          │ Probability Calibration│
          │                        │
          │ - Isotonic Calibration │
          │ - Brier Score          │
          │ - Log Loss Comparison  │
          └───────────┬────────────┘
                      │
                      ▼
          ┌────────────────────────┐
          │ Explainability Layer   │
          │                        │
          │ SHAP Analysis          │
          │                        │
          │ - Feature Impact       │
          │ - Customer Risk        │
          │   Explanation          │
          └───────────┬────────────┘
                      │
                      ▼
          ┌────────────────────────┐
          │ Financial Health Engine│
          │                        │
          │ - Dimension Scoring    │
          │ - Credit Risk Score    │
          │ - Overall Health Score │
          │ - Risk Grade           │
          │ - Loan Readiness       │
          └────────────────────────┘
```

---

## Model Validation

The model was validate on a synthetic MSME dataset generated for research and development purposes.

Evaluation metrics include:
- ROC-AUC
- Precision
- Recall
- F1 Score
- Confusion Matrix
- Calibration metrics (Brier Score and Log Loss)

These evaluations measure the model's ability to learn patterns from the generated dataset and validate the end-to-end ML pipeline.

---
## Financial Health Score Methodology

The Financial Health Score converts MSME financial data and credit risk predictions into an interpretable score that helps assess overall business health and loan readiness.

The score combines two major components:

1. **Business Health Score (50%)**
2. **Credit Risk Score (50%)**

```
                         MSME Financial Data
                                  │
                                  ▼
                    ┌────────────────────────┐
                    │ Feature Processing     │
                    └───────────┬────────────┘
                                │
              ┌─────────────────┴─────────────────┐
              │                                   │
              ▼                                   ▼
┌────────────────────────┐          ┌────────────────────────────┐
│ ML Credit Risk Model   │          │ Business Health Assessment │
│                        │          │                            │
│ XGBoost Classifier     │          │ - Cash Flow Health         │
│                        │          │ - Compliance Health        │
└────────────┬───────────┘          │ - Operational Stability    │
             │                      │ - Digital Adoption         │
             ▼                      │ - Business Stability       │
┌────────────────────────┐          └─────────────┬──────────────┘
│ Probability of Default │                        │
│ (Calibrated PD)        │                        ▼
└────────────┬───────────┘          ┌────────────────────────┐
             │                      │ Business Health Score  │
             ▼                      └────────────┬───────────┘
┌────────────────────────┐                       │
│ Credit Risk Score      │                       │
│ (1 - PD) × 100         │                       │
└────────────┬───────────┘                       │
             │                                   │
             └───────────────┬───────────────────┘
                             ▼
                ┌────────────────────────┐
                │ Financial Health Score │
                │                        │
                │ - Overall Score        │
                │ - Grade                │
                │ - Loan Readiness       │
                └────────────────────────┘

```

---
## API Documentation

This project provides REST APIs through FastAPI for model prediction, financial health assessment, and portfolio analytics.

### Available Endpoints
| Method | Endpoint     | Description |
|--------|--------------|-------------|
| POST   | `/predict`   | Performs complete MSME risk assessment with PD, health score, grade, explanations, and recommendations |
| GET    | `/portfolio` | Retrieves portfolio-level risk insights |
| GET    | `/health`    | API health check |
| GET    | `/`          | API welcome/status endpoint |

---
## Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd msme-financial-health-assessment
```
### 2. Create Virtual Environment
```bash
python -m venv .venv
```
Activate the environment:
```bash
.venv\Scripts\activate #for window
source venv/bin/activate #for linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Backend API
Navigate to the backend directory:
```bash
cd backend
```
Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

API will run at:
```bash
http://localhost:8000
```
Swagger documentation:
```bash
http://localhost:8000/docs
```

### 5. Run Frontend Dashboard
Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
```
Run Streamlit application:
```bash
streamlit run Home.py
```

Dashboard will run at:
```bash
http://localhost:8501
```
---

## Usage
### Individual MSME Assessment
- Enter MSME financial and operational details.
- Generate Probability of Default (PD), Financial Health Score, Credit Grade, explanations and recommendations.

### Portfolio Analytics
- Upload a CSV containing multiple MSMEs.
- Use `data/sample_portfolio.csv` for demo analysis.
- Explore portfolio risk metrics, business insights and high-risk MSME identification.