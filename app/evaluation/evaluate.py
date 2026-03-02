import json
import requests
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall
)
import os
from dotenv import load_dotenv
load_dotenv()
# LLM
from langchain_groq import ChatGroq

# Embeddings
from langchain_huggingface import HuggingFaceEmbeddings


# -------------------------
# 1️⃣ Setup LLM (Directly)
# -------------------------
llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0
)

# -------------------------
# 2️⃣ Setup Embeddings
# -------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -------------------------
# 3️⃣ Load Test Questions
# -------------------------
with open("app/evaluation/testset.json", "r") as f:
    questions = json.load(f)

results = []

# -------------------------
# 4️⃣ Call Your RAG API
# -------------------------
for item in questions:
    q = item["question"]

    response = requests.post(
        "http://localhost:8000/rag/rag",
        params={"query": q}
    )

    if response.status_code != 200:
        print("Error:", response.text)
        continue

    data = response.json()

    if "answer" not in data:
        print("Invalid response:", data)
        continue

    results.append({
        "question": q,
        "answer": data["answer"],
        "contexts": data["contexts"]
    })

# -------------------------
# 5️⃣ Convert to Dataset
# -------------------------
dataset = Dataset.from_dict({
    "question": [r["question"] for r in results],
    "answer": [r["answer"] for r in results],
    "contexts": [r["contexts"] for r in results]
})

# -------------------------
# 6️⃣ Run Evaluation
# -------------------------
score = evaluate(
    dataset,
    metrics=[
        Faithfulness(),
        AnswerRelevancy(),
        ContextPrecision(),
        ContextRecall()
    ],
    llm=llm,
    embeddings=embeddings
)

print("\n===== RAG Evaluation Results =====")
print(score)