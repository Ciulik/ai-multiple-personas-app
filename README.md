# ⚖️ NLP Insights Engine & LLM-as-a-Judge (Interactive Demo)

> **Note:** This repository contains the public interactive demo for a larger, proprietary NLP pipeline maintained privately by a team of developers. This application visualizes the final outputs and evaluations after the data has been processed through the complete backend architecture.

## 📌 Overview
An interactive data visualization application designed to explore structured business insights extracted from unstructured text. This demo showcases the results of a multi-persona generative AI experiment evaluated by an overarching LLM-as-a-Judge module, which utilizes strict mathematical constraints to flag and eliminate generative hallucinations.

## ⚙️ Backend Architecture (Private Pipeline)
The data presented in this demo is the result of a rigorous, private backend pipeline consisting of:
1. **Comparative Sentiment Classification:** Evaluates text using classical models (TF-IDF + Linear SVM) alongside fine-tuned transformer architectures (DistilBERT, RoBERTa), optimized for maximum Micro-F1 performance.
2. **LLM-as-a-Judge with Metric Coupling:** A deterministic safety layer over generative AI outputs. If foundational data accuracy evaluates at ≤2/5, the system mathematically restricts the actionability score, logically blocking the AI from hallucinating business recommendations based on unreliable data.
3. **Aspect-Based Analysis:** Categorizes text into specific operational aspects (e.g., service, price, environment) to route targeted insights.

## 🖥️ Demo Features (This Repository)
- **Interactive Persona Engine:** Toggle between 15+ distinct AI personas (e.g., Data Analyst, Culinary Expert, JSON Strict) to see how different prompt constraints shape the output based on the same foundational data.
- **Judge AI Evaluation Viewer:** Expandable metrics revealing the hidden "LLM Judge" scores for Accuracy (1-5) and Actionability (1-5), including specific feedback on hallucinations.
- **Live Voting & Leaderboard:** Real-time interactive voting system mapping user preferences, visualized dynamically using Plotly.

## 🚀 Tech Stack
- **Frontend / Demo:** Python, Streamlit, Pandas, Plotly Express
- **Backend / Private Core:** scikit-learn, SVM, Hugging Face Transformers (DistilBERT, RoBERTa), PyTorch, Generative LLMs

## 🛠️ How to Run Locally

Follow these steps to deploy the interactive Streamlit demo on your local machine:

**1. Clone the repository:**

git clone [https://github.com/Ciulik/ai-multiple-personas-app.git](https://github.com/Ciulik/ai-multiple-personas-app.git)
cd ai-multiple-personas-app

**2. Install dependencies:**

Ensure you have Python installed, then install the required libraries for the visualization app:
pip install streamlit pandas plotly

**3. Run the application:**

Execute the Streamlit server to launch the app in your default web browser:
streamlit run app.py
