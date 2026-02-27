# 🛡 Social Engineering Risk Scorer

A full-stack AI-powered web application that analyzes social media content and detects potential privacy exposure risks using NLP-based signal extraction.

---

## 🚀 Project Overview

Social Engineering Risk Scorer evaluates publicly shared content and identifies potential vulnerabilities that attackers may exploit through social engineering techniques.

The system analyzes user text and provides:

- 📊 Risk Score (0–100)
- 🚦 Risk Level (Low / Medium / High)
- 📂 Category Breakdown
- 💡 Personalized Recommendations

---

## 🧠 Problem Statement

People unknowingly share sensitive personal information online such as:

- Phone numbers
- Email addresses
- Workplace details
- Travel plans
- Real-time location
- Daily routines

This increases their risk of becoming victims of phishing, impersonation, or targeted attacks.

This tool helps users become aware of their exposure risk.

---


## 🖥️ Tech Stack

### Frontend
- React
- Vite
- TypeScript
- Modern UI components

### Backend
- FastAPI
- Python
- spaCy (NLP processing)
- Custom Risk Scoring Engine

---

## 📂 Project Structure
social-engineering-risk-scorer/

  ── privacy-guard-main/ # React Frontend
  
  ── risk-analyzer-backend/ # FastAPI Backend


---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/social-engineering-risk-scorer.git
cd social-engineering-risk-scorer
```
---
## 2. BackEnd Setup

```bash
cd risk-analyzer-backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Backend runs at:
http://127.0.0.1:8000

## 3. FrontEnd Setup

```bash
cd vite-project
npm install
npm run dev
```
Frontend runs at:
http://localhost:5173

## 🧪 Example

Input:

Leaving home for 10 days. Family alone. Boarding flight at 5AM.

---

## 📊 Features

Real-time text analysis

Category-based exposure breakdown

Context-aware risk scoring

Recommendation engine

Clean modern UI

Full-stack integration

---

## 👩‍💻 Author

AI AVENGERS
Hackathon Project 2026
