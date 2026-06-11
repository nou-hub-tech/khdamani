

https://github.com/user-attachments/assets/fea19085-ce20-40d2-8921-419289b5ce58



#  Khadamni – AI-Powered Recruitment & Employment Analytics Platform

> **What if job hunting was powered by intelligence, not guesswork?**

Khadamni is an intelligent recruitment platform that combines **Machine Learning**, **Data Science**, and **Modern Web Technologies** to improve how candidates and recruiters interact with the job market.

The platform helps users:

* 🔍 Discover relevant job opportunities
* 💰 Estimate expected salaries
* 🌍 Identify the best countries for career mobility
* 🛡️ Detect fraudulent job postings

Built as a full-stack application with dedicated ML services, Khadamni transforms recruitment data into actionable insights.

---

## 🎯 Business Problem

Online recruitment platforms often suffer from:

* Lack of salary transparency
* Irrelevant job recommendations
* Fraudulent job advertisements
* Limited guidance for international career mobility

Khadamni addresses these challenges through data-driven decision making and machine learning models integrated directly into the user experience.

---

## 🧠 Machine Learning Objectives

### 1. Personalized Job Recommendations

Recommend relevant opportunities by grouping similar jobs and candidate profiles.

**Approach**

* Unsupervised Learning
* K-Means Clustering
* DBSCAN

**Selected Model:** K-Means

K-Means produced meaningful and interpretable job clusters, while DBSCAN grouped most jobs into a single cluster and classified many observations as noise.

---

### 2. Best Country Recommendation for Career Mobility

Help professionals identify countries that best match their profile and career goals.

**Approach**

* Country segmentation
* Clustering techniques
* Labor market indicators

**Selected Model:** K-Means

The resulting clusters reveal groups of countries with similar employment and salary characteristics, helping users make informed relocation decisions.

---

### 3. Salary Prediction

Predict expected compensation based on job characteristics.

**Target Variable**

* `salary_in_usd`

**Models Evaluated**

* CatBoost
* XGBoost
* Random Forest

**Selected Model:** CatBoost

Why CatBoost?

* Lower validation RMSE
* Faster convergence
* Better generalization
* Strong handling of categorical features

Key influential features included:

* Job Title
* Experience Level
* Employee Residence
* Company Location
* Employment Type
* Remote Ratio

---

### 4. Fraudulent Job Posting Detection

Detect suspicious job advertisements before they reach candidates.

**Approach**

* Natural Language Processing (NLP)
* TF-IDF Vectorization
* Class Imbalance Handling with SMOTE

**Models Evaluated**

* Logistic Regression
* Random Forest
* XGBoost

**Selected Model:** Logistic Regression

Performance Highlights:

* Accuracy: **99.0%**
* Precision: **91.0%**
* Recall: **87.9%**
* F1-Score: **89.4%**
* ROC-AUC: **99.1%**

The model effectively identifies fraudulent postings while minimizing false alarms.

---

## 📊 Data Science Workflow

The project follows the **CRISP-DM** methodology:

1. Business Understanding
2. Data Understanding
3. Data Preparation
4. Modeling
5. Evaluation
6. Deployment

### Data Preparation Techniques

#### Feature Engineering

* Salary difference from country average
* Employee and company location matching
* Salary normalization

#### Encoding Strategies

* One-Hot Encoding
* Label Encoding
* Target Encoding

#### Dimensionality Reduction

* PCA
* Correlation Analysis

#### NLP Processing

* Text Cleaning
* TF-IDF Vectorization

#### Class Balancing

* SMOTE Oversampling

---

## 🏗️ System Architecture

```text
Frontend (React + TypeScript)
          │
          ▼
Backend API (FastAPI)
          │
 ┌────────┴────────┐
 ▼                 ▼
PostgreSQL      ML Services
Database        (FastAPI)
                     │
                     ▼
      Recommendation Models
      Salary Prediction
      Fraud Detection
      Country Recommendation
```

---

## 💻 Tech Stack

### Frontend

* React
* TypeScript
* Tailwind CSS
* Framer Motion

### Backend

* FastAPI
* Python

### Machine Learning

* Scikit-Learn
* CatBoost
* XGBoost
* Random Forest
* K-Means
* DBSCAN
* TF-IDF
* SMOTE

### Database

* PostgreSQL

### DevOps

* Docker
* Docker Compose

---

## ✨ Platform Features

### For Job Seekers

* User authentication
* Intelligent job recommendations
* Salary prediction
* Best-country suggestions
* Job application management
* Fraud alert system

### For Recruiters

* Job posting management
* Candidate application tracking
* Salary benchmarking insights

---

## 🚀 Quick Start

### Docker (Recommended)

```bash
docker-compose -f docker/docker-compose.yml up -d
```

Initialize the database:

```bash
docker exec -i $(docker-compose -f docker/docker-compose.yml ps -q postgres) \
psql -U khadamni -d khadamni < backend/database/schema.sql
```

### Access the Platform

| Service     | URL                        |
| ----------- | -------------------------- |
| Frontend    | http://localhost:3000      |
| Backend API | http://localhost:8000/docs |
| ML Services | http://localhost:8001/docs |

---

## 📁 Project Structure

```text
Khadamni/
│
├── frontend/          # React application
├── backend/           # FastAPI backend
├── ml_services/       # Machine learning microservices
├── docker/            # Containerization
├── docs/              # Documentation
└── database/          # SQL schema
```

---

## 🔒 Security

* JWT Authentication
* Password Hashing (bcrypt)
* Role-Based Access Control
* Request Validation
* Protected API Endpoints

---

## 📈 Future Improvements

* Deep Learning recommendation engine
* Resume parsing and matching
* Skill gap analysis
* Interview preparation assistant
* Real-time labor market analytics
* LLM-powered career advisor

---

## 👩‍💻 Author

**Nouha Blidi**

Cloud & DevOps Engineer • AI Engineer

Passionate about building intelligent systems that combine Machine Learning, Data Science, Cloud, and modern software engineering to solve real-world problems.

---

## 📜 License

MIT License
