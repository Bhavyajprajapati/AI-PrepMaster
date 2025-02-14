import streamlit as st
import time,PyPDF2,pinecone,json,re
from openai import OpenAI
import google.generativeai as genai
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpointEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_pinecone import PineconeVectorStore
from uuid import uuid4
from langchain_core.documents import Document
from home.TestTopic.Pdf import generate_quiz_zip

pinecone_api_key = "pcsk_ffUJz_7hkW8pZMvpf99EXNU1y65SehYwa2nPKSbrtC8SCZX3mqUGPeYahH6gXpae1SNY6"  # Shivam's Api Key For Vector Store
pinecone_environment = "us-east-1"  
pinecone_index_name = "example-index"

pc = pinecone.Pinecone(api_key=pinecone_api_key)

model_id = "sentence-transformers/all-MiniLM-L6-v2"
hf_token = "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" ## Shivam's Write API for HF 
# api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
# headers = {"Authorization": f"Bearer {hf_token}"}

embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

prompt_RAG_text = ""

HF_API_KEY = "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" ## Read API
API_KEY="AIzaSyAFUFDlRGjxn_VEDn24vQ1BeFnXuoc-SIM" ## Gemini API
openai = OpenAI(api_key=HF_API_KEY, base_url="https://api-inference.huggingface.co/v1")
genai.configure(api_key=API_KEY)

def extract_json(response_text):
    try:
        return json.loads(re.sub(r"```json|```|\\n", "", response_text).strip())
    except json.JSONDecodeError:
        return None

def fetch_questions(text_content, quiz_level, number, extracted_text):
    PROMPT = f"""
        Extract {number} of  MCQs from the following text :\n{extracted_text}\n
        for the following topic {text_content} of level {quiz_level} also
        Generate response with the following JSON format: 
        {{"MCQS": 
            [
                {{"Mcq": "Question here?",
            "Options": {{
                "a": "Choice 1",
                "b": "Choice 2",
                "c": "Choice 3",
                "d": "Choice 4"
                }},
            "Correct_option": "Correct choice letter"
            }}
            ...
            ]
        }}
        please **DO NOT** include any extra explanations or text. Only return the JSON part as shown above. Make sure the response is valid JSON without any additional formatting or extra text.
    """
    ##message = [{"role": "user", "content": PROMPT}]

    try:
        # chat_completion = openai.chat.completions.create(
        #     model="google/gemma-2-2b-it",
        #     messages=[{"role": m["role"], "content": m["content"]} for m in message],
        #     temperature=0.5,
        #     max_tokens=7000,
        #     stream=False,
        # )

        model_name = "models/gemini-1.5-flash"
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(PROMPT)
        res = response.text

        # res = chat_completion.choices[0].message.content
        # st.write(f"Response : {res}")
        cleaned_res = extract_json(res)
        # st.write(f"Cleaned text: {cleaned_res}")
        return cleaned_res.get("MCQS",[])
    except BaseException as e:
        # return jsonify("API error, Max Total Token Allowed is <=8192... Your File is too large"), 399
        return print("API Error!" + str(e)), 399

def display_question():
    """Display all questions and options."""
    questions = st.session_state.quiz_data["questions"]  # Get all questions

    for q_index, question in enumerate(questions):
        a = question['Mcq']
        st.subheader(f"Q{q_index + 1}: {a}")

        # Display radio button for options
        selected_option = st.radio(
            f"Select an answer :",
            options=list(question["Options"].values()),  # Extract values only
            key=f"q_{q_index}",  # Unique key per question
            index=None,  # Allow user to choose, but no default selection
        )

        # Store the selected answer
        st.session_state.quiz_data["selected_options"][q_index] = selected_option
    
    submit_quiz()
    countdown_timer()

def countdown_timer():
    """Countdown Timer for Quiz"""
    if "time_remaining" in st.session_state.quiz_data:
        while st.session_state.quiz_data["time_remaining"] > 0:
            mins, secs = divmod(st.session_state.quiz_data["time_remaining"], 60)
            st.subheader(f"⏳ Time Remaining: {mins}:{secs:02d}")

            time.sleep(1)  # Wait for 1 second
            st.session_state.quiz_data["time_remaining"] -= 1
            st.rerun()  # Rerun Streamlit app to update timer

        # Auto-submit the quiz when time is up
        if not st.session_state.quiz_data["submitted"]:
            auto_submit_quiz()

def auto_submit_quiz():
    """Automatically submits the quiz when the timer runs out"""
    st.session_state.quiz_data["submitted"] = True
    st.session_state.quiz_data["time_remaining"] = 0  # Reset Timer

    # Show thank you message
    st.markdown("## Thank You for Completing the Quiz! 🎉")
    st.balloons()
    marks = 0
    st.header("Quiz Results:")

    questions = st.session_state.quiz_data["questions"]  # Get the list of questions

    for i, question in enumerate(questions):  # Use enumerate for indexing
        selected = st.session_state.quiz_data["selected_options"].get(
            i, "Not Answered"
        )
        correct = question["Options"].get(question["Correct_option"], "Unknown")

        st.write(f"**{question['Mcq']}**")
        st.write(f"Your Answer: {selected}")
        st.write(f"Correct Answer: {correct}")

        if selected == correct:
            marks += 1

    st.subheader(f"Final Score: {marks} / {len(questions)}")

    try:
        # Generate ZIP file containing both PDFs
        zip_buffer = generate_quiz_zip(st.session_state.quiz_data)

        # Download button for ZIP file
        st.download_button(
            label="Download Quiz Files",
            data=zip_buffer,
            file_name="quiz_files.zip",
            mime="application/zip",
        )

    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
    # Reset the quiz state after submission
    st.session_state.quiz_data = {
        "questions": [],
        "selected_options": {},
        "submitted": True,
        "time_remaining": 0,
    }
    st.cache_data.clear()  # Clearing cached data


def submit_quiz():
    if st.button("Submit Quiz", key="Submit"):
        marks = 0
        st.header("Submit Quiz Results:")

        questions = st.session_state.quiz_data["questions"]

        for i, question in enumerate(questions):
            selected = st.session_state.quiz_data["selected_options"].get(i, "Not Answered")
            correct = question["Options"].get(question["Correct_option"], "Unknown")

            st.write(f"**{i+1}**" + " :- " + f"**{question['Mcq']}**")
            st.write(f"Your Answer: {selected}")
            st.write(f"Correct Answer: {correct}")

            if selected == correct:
                marks += 1

        st.subheader(f"Final Score: {marks} / {len(questions)}")

        try:
            # Generate ZIP file containing both PDFs
            zip_buffer = generate_quiz_zip(st.session_state.quiz_data)

            # Download button for ZIP file
            st.download_button(
                label="Download Quiz Files",
                data=zip_buffer,
                file_name="quiz_files.zip",
                mime="application/zip",
            )

        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")

        # Reset the quiz state after submission
        st.session_state.quiz_data = {
            "questions": [],
            "selected_options": {},
            "time_remaining": 0,
            "submitted": True,
        }
        st.cache_data.clear()  # Clearing cached data


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
    st.success("Your Pdf has been Successfully Uploaded...")
    ask_topic_for_test()
    #rerun

def generate_embedding(text):
    text_splitter = SemanticChunker(HuggingFaceEndpointEmbeddings(model=model_id,task="feature-extraction",huggingfacehub_api_token=hf_token),breakpoint_threshold_type="gradient")
    docs = text_splitter.create_documents([text])
    embeddings = HuggingFaceEndpointEmbeddings(model=model_id,task="feature-extraction",huggingfacehub_api_token=hf_token)
    store_in_vector(docs,embeddings)


def upload_pdf():
    text = upload_and_analyze()
    if st.button("Confirm Upload"):
        with st.spinner("Your Pdf is being analyzed, Please Wait..."):
            generate_embedding(text)

def ask_topic_for_test():
    embeddings = HuggingFaceEndpointEmbeddings(model=model_id,task="feature-extraction",huggingfacehub_api_token=hf_token)
    index = pc.Index(pinecone_index_name)
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)

    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = {
            "questions": {},
            "submitted": False,
            "time_remaining": 0,
        }

    user_query = st.text_input("Enter the topic names which you would like to practice :")
    quiz_level = st.selectbox(
        "Select Difficulty:", ["Easy", "Medium", "Hard", "Mix(Easy,Medium,Hard)", "Blooms Taxonomy Based"]
    )
    number = st.slider("Number of Questions:", 5, 30, 10 ,5)
    duration = st.slider("Set Quiz Time (minutes):", 1, 30, 10)  # User sets the timer

    if st.button("Generate Quiz"):
        with st.spinner("Generating Quiz, Please wait..."):
            if user_query:
                results = vector_store.similarity_search(user_query,k=3)
                for res in results:
                    global prompt_RAG_text
                    prompt_RAG_text += res.page_content

                while(True):
                    st.session_state.quiz_data["questions"] = fetch_questions(user_query, quiz_level, number, prompt_RAG_text)
                    if st.session_state.quiz_data["questions"]:
                        break
                    else:
                        continue
                st.session_state.quiz_data["current_index"] = 0
                st.session_state.quiz_data["selected_options"] = {}
                st.session_state.quiz_data["time_remaining"] = (duration * 60)  # Convert minutes to seconds
            else:
                st.warning("Please enter a topic to generate a Quiz.")

    if st.button("Want to upload another Pdf"):
        st.session_state['uploaded_and_analyzed'] = False
        upload_pdf()

    if st.session_state.quiz_data["questions"]:
        display_question()
    # rerun

def test_with_your_material_interface():
    if st.session_state["uploaded_and_analyzed"]:
        ask_topic_for_test()
    else:
        upload_pdf()

    if st.session_state.quiz_data["questions"]:
        display_question()
