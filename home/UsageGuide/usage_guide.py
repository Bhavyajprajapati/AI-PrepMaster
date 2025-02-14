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
## 📘 User Manual for Learning Assistance Feature
### Step 1: 📝 Enter a Topic
- Navigate to the **Learn** section on the website.
- Enter the study-related topic you want to learn.
- Click the **Learn** button to generate relevant learning material.

### Step 2: 📄 Download Learning Material
- After the content is displayed, you can download it as a PDF.
- Click the **Download** button at the end of the page to save the material for offline use.

## ⚠️ Constraints & Guidelines
- **Ensure Proper Topic Entry**: Enter a **clear and concise topic** to get the best results.
- **Study-Related Topics Only**: The system is optimized for academic and educational topics.

For assistance, contact **📧 AipreapMaster@gmail.com**.

---

## 🎯 Conclusion
By following these steps and guidelines, users can efficiently process OMR sheets and learn about various study topics. If you encounter any issues, refer to the troubleshooting section or reach out to support. Happy learning & evaluating!


    
        """
        st.markdown(content,unsafe_allow_html=True)
    
    elif selected_usage_option == "OMR checking":
        
        content = """
            ### 📘 User Manual for OMR Checking

## 🌟 Introduction
Welcome to our OMR Processing section! This section allows users to generate and evaluate OMR sheets efficiently. Follow the steps below to ensure accurate processing.

## 🚀 Steps to Use

### Step 1: 📥 Download Sample PDF
- Download the sample PDF from the sidebar according to your requirement.

### Step 2: ✍️ Create Your Question Paper
You have two options:
1. **Create your own question paper** manually.
2. **Use our services from sidbar**:
   - Generate a test based on a topic or upload your own material.
   - You will receive a **question paper, answer key for OMR checking, and solution** for the paper.

### Step 3: 📤 Upload Your OMR Sheets
- Navigate to the **OMR Checking** section.
- Upload your **filled OMR sheets** (images or PDFs).
- You can upload a mix of images and PDFs.
- Ensure that the images are **clear**, with no **shadows** over the OMR.

### Step 4: 🔢 Select Evaluation Criteria
- Enter the **number of questions**, **negative marking count**, and **number of options** per question.

### Step 5: 📌 Provide Answer Key
- **If using our generated question paper**: Simply paste the **provided answer key**.
- **If checking your own paper**: Enter the correct answers separated by commas (e.g., **A,B,C**). Ensure:
  - All answers are in **capital letters**.
  - The answers match the selected **number of options**.

### Step 6: ✅ Click Check
- Click the **Check** button to start processing.
- The system will evaluate all **pages of PDFs and images**.
- A **live panel** will display real-time processing updates.
- The processed results will be compiled into a **downloadable PDF**.

## ⚠️ Constraints & Guidelines
- **Image & PDF Quality**: Ensure clarity, no shadows, and proper alignment.
- **OMR Format**: Use only **predefined templates provided by us**.
- **Filling Instructions**: Use a **black or blue pen** and fully mark bubbles.
- **File Size Limit**: Maximum **10 MB** per file.

For assistance, contact **📧 AipreapMaster@gmail.com**.

---

## 🎯 Conclusion
By following these steps and guidelines, users can efficiently process OMR sheets with accurate results. If you encounter any issues, refer to the troubleshooting section or reach out to support. Happy evaluating!

        """
        st.markdown(content,unsafe_allow_html=True)
