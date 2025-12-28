# Ops Workflow Automation Platform  
**End-to-End Data Ingestion, Validation, Orchestration & Analytics Pipeline**

---

## 📌 Overview

This project is a **production-grade data workflow automation platform** designed to simulate how modern analytics teams ingest, validate, version, orchestrate, and analyze data at scale.

It combines **FastAPI**, **PostgreSQL**, **Apache Airflow**, **Streamlit**, and **Docker** to deliver a fully automated, analyst-friendly data pipeline with strong emphasis on **data quality, reliability, and reproducibility**.

The system is built to mirror **real-world data engineering & analytics workflows** used in fintech, SaaS, and product analytics teams.

---

## 🎯 Key Objectives

- Ensure **high-quality, trusted data** through automated validation
- Enable **idempotent & incremental data loads**
- Maintain **dataset versioning & metadata tracking**
- Provide **self-serve data quality dashboards** for analysts
- Orchestrate workflows reliably using **Airflow**
- Reduce manual operations, latency, and data errors

---

## 🏗️ Architecture

Streamlit UI
|
| (CSV Upload)
v
FastAPI (Upload & Validation Service)
|
|-- Schema Validation
|-- Deduplication
|-- Dataset Versioning
|-- Data Quality Metrics
|
v
PostgreSQL (Analytics Warehouse)
|
v
Apache Airflow (Workflow Orchestration)
|
v
Downstream Transformations & Loads



All services run in **isolated Docker containers** using `docker-compose`.

---

## ⚙️ Tech Stack

| Layer | Technology |
|------|-----------|
Backend API | **FastAPI**
Database | **PostgreSQL**
Workflow Orchestration | **Apache Airflow**
Frontend Dashboard | **Streamlit**
Data Processing | **Pandas**
Containerization | **Docker & Docker Compose**
ORM | **SQLAlchemy**

---

## 🚀 Features

### ✅ Data Ingestion
- Upload raw CSV datasets via Streamlit UI
- FastAPI handles ingestion with schema enforcement

### ✅ Data Validation & Quality Checks
- Schema validation
- Null percentage calculation
- Duplicate row detection
- Checksum-based deduplication

### ✅ Dataset Versioning & Metadata
- Automatic dataset versioning per filename
- Metadata tracking:
  - Row counts
  - Checksums
  - Upload timestamps

### ✅ Incremental & Idempotent Loads
- Prevents duplicate inserts
- Safe re-runs without corrupting data
- Ensures consistent reporting

### ✅ Workflow Orchestration
- Automatically triggers Airflow DAG on successful upload
- Enables downstream transformations & analytics jobs

### ✅ Data Quality Dashboard
- Streamlit dashboard showing:
  - Null percentages
  - Duplicate rows
  - Dataset freshness
  - Upload history
- Built for analysts & non-technical stakeholders

---

## 📂 Project Structure

ops_workflow_automation/
│
├── api/
│ └── upload_service.py # FastAPI backend
│
├── dag/
│ └── ops_workflow_automation_dag.py
│
├── ui/
│ └── ops_uploader.py # Streamlit dashboard
│
├── raw_data/ # Sample input data
│
├── validation.py # Data validation logic
├── ingest.py
├── transformation.py
├── load_to_postgres.py
├── create_table.sql # DB schema
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md



---

## 🧪 How the Pipeline Works (Step-by-Step)

1. User uploads a CSV via **Streamlit UI**
2. FastAPI:
   - Validates schema
   - Computes data quality metrics
   - Checks for duplicates using checksums
3. Metadata & quality metrics stored in PostgreSQL
4. Data loaded incrementally into analytics tables
5. Airflow DAG is auto-triggered for downstream jobs
6. Analysts monitor data quality via Streamlit dashboard

---

## 🛠️ Setup Instructions

### Prerequisites
- Docker & Docker Compose
- Git

---

### Clone the Repository
```bash
git clone https://github.com/Advait-sankar/Ops_workflow_automation.git
cd Ops_workflow_automation
```
### ▶️ Start the Platform

```bash
docker-compose up --build
```

### 📊 Use Cases
1. Data Analyst: Monitor data quality, freshness, and anomalies
2. Business Analyst: Trust metrics, dashboards, and reporting inputs
3. Product Analyst: Reliable experiment data and KPI pipelines
4. Data Engineer: Orchestrate, monitor, and scale workflows


### 📈 Why This Project Matters
This project demonstrates:
    1. Real-world analytics engineering practices
    2. Strong data quality ownership and validation
    3. Production-ready workflow orchestration with Airflow
    4. Analyst-first, self-serve dashboards
    5. End-to-end system thinking, not just scripts
It is intentionally designed to align with Data Analyst, Business Analyst, and Product Analyst roles in modern data-driven organizations.

