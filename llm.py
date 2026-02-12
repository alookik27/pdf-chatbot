import ollama

def generate_answer(query, retrieved_chunks):
    context = "/n/n".join(retrieved_chunks)
    prompt = f"""
you are an assistant answering questions based ONLY on the context provided.

Context:
{context}

Question:
{query}

Answer cleary and concisely using only he context above.
"""
    
    response = ollama.chat(
        model = "phi3",
        messages=[{"role": "user","content":prompt}]
    )

    return response["message"]["content"]
