# Predictive Churn Pipeline & ROI Optimization Engine using XGBoost

An industry-grade, end-to-end MLOps pipeline designed to predict customer churn in the telecommunications sector, automate data validation and versioning, and translate machine learning probabilities into actionable financial strategies (CLV & Campaign ROI).

---

## 🚀 Project Overview
Traditional churn models stop at classification—predicting whether a customer will leave or stay. This project bridges the gap between data science and business economics by integrating a custom financial engine that quantifies **Customer Lifetime Value (CLV)** and evaluates the net profit and **ROI of targeted retention campaigns**.

The entire workflow is orchestrated using **DVC (Data Version Control)** to ensure full reproducibility and automated execution from raw data ingestion to impact reporting.

---

## 🛠️ Tech Stack
* **Core Language:** Python 3.9+
* **Machine Learning:** XGBoost, Scikit-Learn
* **Explainable AI:** SHAP (SHapley Additive exPlanations)
* **MLOps & Version Control:** DVC, Git
* **Data Validation:** Pandera
* **Automation & Architecture:** Modular design, structured pipelines

---

## 📂 Project Architecture

telco-churn-roi-pipeline/
├── config/                 # Configuration parameters
├── data/                   # DVC-tracked data storage (Raw, Processed)
├── reports/                # Generated SHAP charts and business impact reports
├── src/                    # Core source code
│   ├── business_engine/    # CLV and ROI campaign cost-benefit calculations
│   ├── data_pipeline/      # Automated ingestion and Pandera validation schemas
│   ├── features/           # Feature engineering and cleaning scripts
│   └── models/             # XGBoost training and SHAP explainability modules
├── dvc.yaml                # Master DVC pipeline orchestrator
└── pyproject.toml          # Modern dependency and packaging management

---

## 📈 Pipeline Stages & Workflow

1. **Data Ingestion (`ingest.py`):** Programmatically connects to the Kaggle API to pull the IBM Telco Customer Churn dataset.
2. **Data Validation (`validate.py`):** Acts as an automated quality-control bouncer using **Pandera** to enforce schema rules, preventing data drift or formatting errors from entering the model.
3. **Feature Engineering (`build_features.py`):** Handles missing values, encodes target variables, and derives economic metrics like tenure years.
4. **Model Training (`train_xgboost.py`):** Trains an optimized XGBoost classifier using dynamic class-weight balancing (`scale_pos_weight`) to maximize recall on minority churn classes.
5. **Explainability (`explain_shap.py`):** Utilizes game-theory-based SHAP values to isolate the primary behavioral drivers behind customer attrition.
6. **Business Impact Engine (`roi_optimizer.py`):** Simulates retention campaign economics, balancing intervention costs against saved Customer Lifetime Value (CLV).

---

## 📊 Business Impact & Results
* **High-Risk Identification:** Optimized classification model tracking high-propensity churners.
* **Cost-Benefit Simulation:** Evaluates targeted retention budgets (e.g., $20/user) against predicted revenue savings over a 6-month horizon, generating automated financial impact statements in `reports/business_impact.txt`.

---

## ⚙️ Quick Start

**1. Clone the repository:**
git clone https://github.com/pavan10994/Predictive-Churn-Pipeline-ROI-optimization-engine-using-XGBOOST.git
cd Predictive-Churn-Pipeline-ROI-optimization-engine-using-XGBOOST

**2. Set up the virtual environment and install dependencies:**
python -m venv venv
venv\Scripts\activate
pip install -e .

**3. Run the automated pipeline via DVC:**
dvc repro