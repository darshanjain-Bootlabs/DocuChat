from groq import Groq

from app.services.vector_service import similarity_search

client = Groq()
MODEL_NAME = "llama-3.1-8b-instant"

def build_context(query:str) -> str:
    context = []

    for i,doc in enumerate(similarity_search(query,k=3)):
        context.append(f"[source: doc_{i}] {doc.page_content}")
    
    return "\n".join(context)

def build_prompt(query: str,context: str) -> str:
    prompt = f"""
    You are an AI assistant answering questions based strictly on the provided context.

Guidelines:
- Use ONLY the information from the context.
- Do not make assumptions or add external knowledge.
- If the answer is not found in the context, say: "Information not found in retrieved context."
- Keep the response clear, structured, and directly relevant to the question.
- Do not provide recommendations unless explicitly asked.
- For every key claim, ensure it is directly supported by the context.Do not generalize beyond the retrieved content.

Structure your response as follows:

1. Overview  
   Provide a brief summary directly addressing the question.

2. Detailed Explanation  
   Expand on the answer using relevant information from the context.

3. Key Points (if applicable)  
   List important points clearly in bullet format when useful.
    
    Context:
    {context}
    
    Answer:
    {query}
    """
    return prompt

def generate_response(query: str):
    docs = similarity_search(query, k=3)
    context = build_context(query)
    prompt = build_prompt(query, context)
    rresponse = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.1,
    )
    answer = rresponse.choices[0].message.content

    return {
        "answer": answer,
        "sources": [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
            }
            for doc in docs
        ]
    }