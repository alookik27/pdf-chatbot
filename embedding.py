from sentence_transformers import SentenceTransformer
import numpy as np
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embeddings(text_chunks):
    
    embeddings = model.encode(text_chunks)
    embeddings = np.array(embeddings)
    if embeddings.ndim ==1:
        embeddings = embeddings.reshape(1,-1)
    return embeddings

