# ⚖️ NLP Insights Engine & LLM-as-a-Judge Validation

## 📌 Overview
An advanced Natural Language Processing pipeline designed to extract structured business insights from unstructured text. This repository features a comparative sentiment classification engine and an LLM-as-a-Judge module that utilizes strict mathematical constraints to eliminate generative hallucinations.( this is only the demo part of the actual code that is private behind a team of developers, the demo uses the data after it was throughout the whole pieline and shows the final results)

## ⚙️ Architecture

1. **Comparative Sentiment Classification**
   - Evaluates text using classical models (TF-IDF + Linear SVM) alongside fine-tuned transformer architectures (DistilBERT, RoBERTa).
   - Benchmarked on datasets to identify optimal contextual understanding versus computational cost.

2. **LLM-as-a-Judge with Metric Coupling**
   - Implements a deterministic safety layer over generative AI outputs.
   - **Metric Coupling Logic:** If the foundational data accuracy is evaluated at ≤2/5 by the system, the actionability score is automatically restricted. 
   - **Result:** The system is mathematically blocked from hallucinating business recommendations based on invented or low-confidence data.

3. **Aspect-Based Analysis**
   - Categorizes text into specific operational aspects (e.g., service, price, ambiance) to route targeted insights rather than relying on generic sentiment scores.

## 🚀 Tech Stack
- **Machine Learning:** scikit-learn, SVM, TF-IDF
- **Deep Learning / NLP:** Hugging Face Transformers (DistilBERT, RoBERTa), PyTorch
- **Generative AI:** LLM integration via prompt engineering guardrails
- **Languages:** Python
