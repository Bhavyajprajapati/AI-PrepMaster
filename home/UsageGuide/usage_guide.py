import streamlit as st

def usage_guide_interface():
    # if st.session_state["logged_in"]:
    #     st.subheader("How to use")
    
    # usage = """
    # <h4>
    #     <b>Select your interst from sidebar First</b>
    # </h4>
    
    # """
    # st.markdown(usage,unsafe_allow_html=True)
    
    usage_options=['Learn particular topic', 'Test with topics',
                    'Test with your own material','OMR checking']
    
    
    selected_usage_option = st.selectbox("Require guide for:",usage_options,index=0)
    
    if selected_usage_option == "Learn particular topic":
        content = """
            ## 📘 User Guide for Topic Mastery zone

## ✨ Introduction
Welcome to **Ai-prepMaster**, your interactive learning companion! This guide provides step-by-step instructions on how to use the platform to generate topic-based educational content, save responses, and download them in various formats.

## 🌟 Features
-  Generate detailed explanations for any topic.
-  Response according to prviously enterd topic.
-  Convert responses into **📄 PDF** and **📝 Word documents** for offline use.
-  Interactive UI for a seamless learning experience.

## 📖 How to Use

#### Open the **Topic mastery zone 🚀** from sidebar.
### 1️⃣ Enter a Topic to Learn
-  Enter a topic of interest in the input field.
-  Click the **Learn** button to generate a structured response.

### 2️⃣ Reviewing the Generated Response
-  The application displays detailed educational content based on the topic entered.
-  If previous topics were generated, they will be shown in the **communication history**.

### 3️⃣ Generating and Downloading Documents
-  Click **Generate PDF** to save the conversation as a PDF.
-  Click **Generate Word Document** to download it as a DOCX file.
-  The files are automatically formatted for easy reading and printing.

### 4️⃣ Continue Learning
-  Click **Next Input** to enter a new topic and continue learning.


## 🛠️ Troubleshooting
##### Issue: No Response Generated
-  Verify your internet connection.
-  Ensure the service is operational.
-  Try simplifying your topic input.

## 🎯 Conclusion
**Ai-prepMaster** is a powerful tool for structured learning and document generation. Explore various topics and save your knowledge effortlessly! 🚀



    
        """
        st.markdown(content,unsafe_allow_html=True)
    
    elif selected_usage_option == "OMR checking":
        
        content = """
            ### 📘 User guide for OMR Checking

## 🌟 Introduction
Welcome to our OMR Processing section! This section allows users to generate and evaluate OMR sheets efficiently. Follow the steps below to ensure accurate processing.

## 🚀 Steps to Use

### 1️⃣ Download Sample PDF
- Download the sample PDF from the sidebar according to your requirement.

### 2️⃣ Create Your Question Paper
You have two options:
1. **Create your own question paper** manually.
2. **Use our services from sidbar**:
   - Generate a test based on a topic or upload your own material.
   - You will receive a **question paper, answer key for OMR checking, and solution** for the paper.

### 3️⃣ Upload Your OMR Sheets
- Navigate to the **OMR Checking** section.
- Upload your **filled OMR sheets** (images or PDFs).
- You can upload a mix of images and PDFs.
- Ensure that the images are **clear**, with no **shadows** over the OMR.

### 4️⃣ Select Evaluation Criteria
- Enter the **number of questions**, **negative marking count**, and **number of options** per question.

### 5️⃣ Provide Answer Key
- **If using our generated question paper**: Simply paste the **provided answer key**.
- **If checking your own paper**: Enter the correct answers separated by commas (e.g., **A,B,C**). Ensure:
  - All answers are in **capital letters**.
  - The answers match the selected **number of options**.

### 6️⃣ Click Check
- Click the **Check** button to start processing.
- The system will evaluate all **pages of PDFs and images**.
- A **live panel** will display real-time processing updates.
- The processed results will be compiled into a **downloadable PDF**.

## ⚠️ Constraints & Guidelines
- **Image & PDF Quality**: Ensure clarity, no shadows, and proper alignment.
- **OMR Format**: Use only **predefined templates provided by us**.
- **Filling Instructions**: Use a **black or blue pen** and fully mark bubbles.
- **File Size Limit**: Maximum **30 MB** per file.

For assistance, contact **📧 AipreapMaster@gmail.com**.

---

## 🎯 Conclusion
By following these steps and guidelines, users can efficiently process OMR sheets with accurate results. If you encounter any issues, refer to the troubleshooting section or reach out to support. Happy evaluating!

        """
        st.markdown(content,unsafe_allow_html=True)
