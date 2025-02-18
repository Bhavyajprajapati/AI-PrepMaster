import streamlit as st
import time,PyPDF2,pinecone
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from uuid import uuid4
from langchain_core.documents import Document

pinecone_api_key = "pcsk_ffUJz_7hkW8pZMvpf99EXNU1y65SehYwa2nPKSbrtC8SCZX3mqUGPeYahH6gXpae1SNY6"  # Shivam's Api Key For Vector Store
pinecone_environment = "us-east-1"  
pinecone_index_name = "example-index"
pc = pinecone.Pinecone(api_key=pinecone_api_key)
model_id = "sentence-transformers/all-MiniLM-L6-v2"
hf_token = "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"

def upload_and_analyze():
    uploaded_file = st.file_uploader("Upload the PDF file only",type=['pdf'])
    r_text = ""
    if uploaded_file is not None:
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            for page_num in range(len(reader.pages)):
                r_text += reader.pages[page_num].extract_text()

            st.session_state['pdf_uploaded'] = True
        except:
            st.error("This file is unable to read!!!")
            r_text = ""
    return r_text

def store_in_vector(docs,embeddings):
    if pinecone_index_name not in pc.list_indexes().names():
        pc.create_index(
            name=pinecone_index_name,
            dimension=384,
            metric='cosine',
            spec=pinecone.ServerlessSpec(cloud='aws', region=pinecone_environment)
        )
        while not pc.describe_index(pinecone_index_name).status["ready"]:
            time.sleep(1)
    
    index = pc.Index(pinecone_index_name)
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)
    documents = [Document(page_content = doc.page_content, metadata={"source": "general pdf data"},) for doc in docs]
    uuids = [str(uuid4()) for _ in range(len(documents))]

    vector_store.add_documents(documents=documents, ids=uuids)
    st.session_state["uploaded_and_analyzed"] = True
    st.rerun()

def generate_embedding(text):
    # text_splitter = SemanticChunker(HuggingFaceEndpointEmbeddings(model=model_id,task="feature-extraction",huggingfacehub_api_token=hf_token),breakpoint_threshold_type="gradient")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2330,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )
    docs = text_splitter.create_documents([text])
    embeddings = HuggingFaceEndpointEmbeddings(model=model_id,task="feature-extraction",huggingfacehub_api_token=hf_token)
    store_in_vector(docs,embeddings)

def upload_pdf():
    text = upload_and_analyze()
    if text:
        with st.spinner("Your Pdf is being analyzed, Please Wait..."):
            generate_embedding(text)

def material_uploader_interface():
    if st.session_state["uploaded_and_analyzed"]:
        st.success("Your pdf has been successfully uploaded, Now you can go to Test with your own material option to get Quiz.")
        if st.button("Want to upload another Pdf"):
            st.session_state['uploaded_and_analyzed'] = False
            upload_pdf()
    else:
        upload_pdf()