import streamlit as st
from pdf_loader import extract_text_from_pdf
from text_splitter import split_text
from embedding import get_embeddings
from vector_store import create_faiss_index, search_index
from llm import stream_answer


st.set_page_config(page_title="PDF-Chatbot",layout="centered")
st.title("📄 PDF Chatbot")
st.write("Upload a pdf and asks questions 🥸")

uploaded_files = st.file_uploader("",type=["pdf"], accept_multiple_files=True)

if uploaded_files :
        st.info("click the button to process the pdfs")
        for file in uploaded_files:
       
         all_chunks = []
        if st.button("Process the pdf"):
         
         with st.spinner(f"Reading {file.name} ..."):
          
          for file in uploaded_files:
           text = extract_text_from_pdf(file)
           chunks = split_text(text, 350, 50)
           all_chunks.extend(chunks)
        st.success(f"PDF splits into {len(all_chunks)} chunks")
      ### this was the code for printing chunks 

       ### for i, chunk in enumerate(chunks[:3]):
       ###      st.text(f"chunk {i+1} : \n{chunk}")
      
      ### end
      

       ### this is the code for creating embedding using the file embedding.py in which i used sentenced transformer.   
      
        ###st.write("creating embeddings...")
        chunks_embeddings= get_embeddings(all_chunks)
        index = create_faiss_index(chunks_embeddings)
        st.session_state.chunks = all_chunks
        st.session_state.index = index
      
       ### end
        

        if "index" in st.session_state:
            st.divider()
            query = st.text_input("Ask a Question about the PDFs")
        if query:
            query_embedding = get_embeddings([query])
            indices = search_index(st.session_state.index, query_embedding, k = 2)

            retrieved_chunks = [
                st.session_state.chunks[int(idx)] for idx in indices[0]
            ]

            st.subheader("Retrieved Context:")
            for chunk in retrieved_chunks:
                st.write(chunk)

            st.subheader("AI Answer:")

            response_placeholder = st.empty()
            full_response = ""
            for tokens in stream_answer(query, retrieved_chunks):
                full_response += tokens
                response_placeholder.markdown(full_response + "🧠")

### this was the code for direct answer generation

           ### with st.spinner("thinking..."):
           ###     answer = generate_answer(query, retrieved_chunks)
           ###     st.write(answer)

###. end. 

