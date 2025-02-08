import streamlit as st
import os


def download_omr_interface():
    st.subheader("OMR Downloader")

    num_questions = st.selectbox("Select number of questions:", [10, 15, 20, 25, 30])
    num_choices = st.selectbox("Select number of choices:", [4, 5])
    fname = f"OMR_Test_{num_questions}_{num_choices}.pdf"
    file_map = {
        (10, 4): "media_files/sample_pdfs/MCQ_Test_10_4_C.pdf",
        (10, 5): "media_files/sample_pdfs/MCQ_Test_10_5_C.pdf",
        (15, 4): "media_files/sample_pdfs/MCQ_Test_15_4_C.pdf",
        (15, 5): "media_files/sample_pdfs/MCQ_Test_15_5_C.pdf",
        (20, 4): "media_files/sample_pdfs/MCQ_Test_20_4_C.pdf",
        (20, 5): "media_files/sample_pdfs/MCQ_Test_20_5_C.pdf",
        (25, 4): "media_files/sample_pdfs/MCQ_Test_25_4_C.pdf",
        (25, 5): "media_files/sample_pdfs/MCQ_Test_25_5_C.pdf",
        (30, 4): "media_files/sample_pdfs/MCQ_Test_30_4_C.pdf",
        (30, 5): "media_files/sample_pdfs/MCQ_Test_30_5_C.pdf",
    }

    file_path = file_map.get((num_questions, num_choices))

    
    if file_path and os.path.exists(file_path):
        with open(file_path, "rb") as f:
            st.download_button(
                label="Download PDF",
                data=f,
                file_name=fname,
                mime="application/pdf"
            )
    else:
        st.error("Selected PDF file not found.")
