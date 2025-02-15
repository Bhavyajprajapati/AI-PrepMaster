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

#### 📌 Open the **Topic mastery zone** from sidebar.
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
-  For assistance, contact 📧 AipreapMaster@gmail.com.
## 🎯 Conclusion
**Ai-prepMaster** is a powerful tool for structured learning and document generation. Explore various topics and save your knowledge effortlessly! 🚀



    
        """
        st.markdown(content,unsafe_allow_html=True)
    
    elif selected_usage_option == "OMR checking":
        
        content = """
            ## 📘 User guide for OMR Checking

## 🌟 Introduction
Welcome to our OMR Processing section! This section allows users to generate and evaluate OMR sheets efficiently. Follow the steps below to ensure accurate processing.

## 🚀 Steps to Use
#### 📌 Open the download thesample pdf from the sidebar
### 1️⃣ Download Sample PDF
- According to your requirement download OME sheet.

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
    elif selected_usage_option == "Test with topics":
        content = """
        ## 📘 User Guide for MCQ Test Generation

## ✨ Introduction

Welcome to **AI-PrepMaster**, your smart MCQ test generator! This guide will help you navigate through the test creation process, customize your quiz settings, and download results efficiently.

## 🌟 Features

- Select a topic for your MCQ test.
- Choose the **number of questions** for the test.
- Set a **time limit** for the test.
- Select a **difficulty level**:
- Instant result evaluation with correct answers.
- **Downloadable PDFs** in multiple formats.

---

## 📖 How to Use
#### 📌 Open the **Test with topic** from sidebar.
### 1️⃣ Select a Topic

- Choose a topic from the available list or enter your own.
- Click **Generate Test** to proceed.

### 2️⃣ Configure Test Settings

- Select the **number of questions**.
- Set a **time limit** for completion.
- Choose the **difficulty level**:
  - Easy, Medium, Hard, Mix
  - BT-Based (Remember, Understand, Apply)

### 3️⃣ Start the Test

- Click **Start Test**.
- Answer the MCQs. You can leave a question blank if unsure.
- The test can be submitted using submit button at bottom or it will **automatically submits** when the timer runs out.

### 4️⃣ Submission and Instant Results

- After submission, you receive **instant feedback**:
  - Correct answers are displayed.
  - You can download all the files at same time in zip format by clicking download files button.

### 5️⃣ Download Results

- you will get the following PDFs in zip:
  1. **quiz\_answer.pdf** – Contains only the correct answers.
  2. **quiz\_with\_response.pdf** – Highlights your selected answers:
     - **Green**: Correct
     - **Red**: Incorrect
     - **Yellow highlight**: Correct answer
  3. **quiz\_question.pdf** – Contains only the test questions.
  4. **answer\_key.txt** – Provides an answer key for reference.
- You can use the files 3 and 4 for conducting OMR test.
---

## 🛠️ Future Updates

- Multiple-mark questions will be available soon!
- More customization options for test settings like negative marking will be also added.

---

## 🎯 Conclusion

With **AI-PrepMaster**, you can efficiently test your knowledge, track your performance, and download structured reports. Start mastering topics today!
For assistance, contact 📧 AipreapMaster@gmail.com.

        """
        st.markdown(content,unsafe_allow_html=True)
    elif selected_usage_option == "Test with your own material":
        content="""
        ## 📘 User Guide for MCQ Test Generation from your own material

## ✨ Introduction

Welcome to **AI-PrepMaster**, your smart MCQ test generator! This guide will help you navigate through the test creation process, customize your quiz settings, and download results efficiently.

## 🌟 Features

- **Upload your own PDF material** to generate an MCQ test.
- Choose the **number of questions** for the test.
- Set a **time limit** for the test.
- Select a **difficulty level**:
- Instant result evaluation with correct answers.
- **Downloadable PDFs** in multiple formats.

---

## 📖 How to Use
#### 📌 Open the **Upload your material** from sidebar.
### 1️⃣ Upload Your Study Material

- Click **Upload PDF** and select your document.
- File size must be less than 10Mb.
- Click **Confirm upload** to proceed.
- It will proccess your pdf 
- If you want to upload another pdf then you can click want to upload another pdf
- Only after pdf uploaded and processed you can test with it. 

### 2️⃣ Configure Test Settings
#### 📌 Now open the **Test with your material** from sidebar.
- Enter the topics from which you want to generate MCQs only from your pdf.
- Select the **number of questions**.
- Set a **time limit** for completion.
- Choose the **difficulty level**:
  - Easy, Medium, Hard, Mix
  - BT-Based (Remember, Understand, Apply)

### 3️⃣ Start the Test

- Click **Start Test**.
- Answer the MCQs. You can leave a question blank if unsure.
- The test can be submitted using the **Submit** button at the bottom or it will **automatically submit** when the timer runs out.

### 4️⃣ Submission and Instant Results

- After submission, you receive **instant feedback**:
  - Correct answers are displayed.
  - You can download all the files at the same time in **ZIP format** by clicking the **Download Files** button.

### 5️⃣ Download Results

- You will get the following PDFs in a ZIP file:
  1. **quiz\_answer.pdf** – Contains only the correct answers.
  2. **quiz\_with\_response.pdf** – Highlights your selected answers:
     - **Green**: Correct
     - **Red**: Incorrect
     - **Yellow highlight**: Correct answer
  3. **quiz\_question.pdf** – Contains only the test questions.
  4. **answer\_key.txt** – Provides an answer key for reference.
- You can use files 3 and 4 for conducting an **OMR test**.

---

## 🛠️ Future Updates

- Multiple-mark questions will be available soon!
- More customization options for test settings like negative marking will be added.

---

## 🎯 Conclusion

With **AI-PrepMaster**, you can efficiently generate tests from your own study material, track your performance, and download structured reports. Start mastering topics today!
For assistance, contact 📧 AipreapMaster@gmail.com.
"""
        st.markdown(content,unsafe_allow_html=True)
