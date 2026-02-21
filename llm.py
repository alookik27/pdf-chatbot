import ollama

###def generate_answer(query, retrieved_chunks):
###    context = "/n/n".join(retrieved_chunks)
###    prompt = f"""
###you are an assistant answering questions based ONLY on the context provided.
###
###Context:
###{context}
###
###Question:
###{query}
###
###Answer cleary and concisely using only he context above.
###"""
###    
###    response = ollama.chat(
###        model = "phi3",
###        messages=[{"role": "user","content":prompt}]
###    )
###
###    return response["message"]["content"]


def stream_answer(query, retrieved_chunks):
    context = "\n\n".join(retrieved_chunks)
    prompt = f"""
You are an assistant answering questions based ONLY on the context provided. 
And if the context contains headings, ignore them. 
Focus only on the meaningful explaination

Context:
{context}

Question:
{query}

Answer cleary and concisely using only the context above. 
"""
    
    stream = ollama.chat(
        model = "phi3",
        messages = [{"role":"user", "content":prompt}],
        stream = True
    )

    for chunk in stream:
        yield chunk["message"]["content"]
