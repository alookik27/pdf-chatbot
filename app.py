import streamlit as st
from pdf_loader import extract_text_from_pdf
from text_splitter import split_text
from embedding import get_embeddings
from vector_store import create_faiss_index, search_index
from llm import generate_answer


st.set_page_config(page_title="PDF-Chatbot",layout="centered")
st.title("📄 PDF Chatbot")
st.write("Upload a pdf and asks questions [soon]")

uploaded_file= st.file_uploader("Uploade a PDF",type=["pdf"])

if uploaded_file :
    st.info("click the button to process the pdf")
    if st.button("Process the pdf"):
 
        with st.spinner("Reading Pdf..."):
            text = extract_text_from_pdf(uploaded_file)
        st.write("total characters in pdf:",len(text))

        chunk_size=200
        overlaps=50
        
        st.write("chunk size",chunk_size)
        st.write("Overlaps:",overlaps)

        chunks = split_text(text,chunk_size,overlaps)

        st.write("Total chunks:",len(chunks))
        st.success(f"PDF splits into {len(chunks)} chunks")
        for i, chunk in enumerate(chunks[:3]):
             st.text(f"chunk {i+1} : \n{chunk}")

        st.write("creating embeddings...")
        chunks_embeddings= get_embeddings(chunks)
        index = create_faiss_index(chunks_embeddings)
        st.session_state.chunks = chunks
        st.session_state.index = index
        st.success("Embeddings are stored in faiss now!")
        
    if "index" in st.session_state:
        query = st.text_input("Ask a Question about the PDF")
        if query:
            query_embedding = get_embeddings([query])
            indices = search_index(st.session_state.index, query_embedding)

            retrieved_chunks = [
                st.session_state.chunks[int(idx)] for idx in indices[0]
            ]

            st.subheader("Retrieved Context:")
            for chunk in retrieved_chunks:
                st.write(chunk)

            st.subheader("AI Answer:")
            with st.spinner("thinking..."):
                answer = generate_answer(query, retrieved_chunks)
                st.write(answer)



