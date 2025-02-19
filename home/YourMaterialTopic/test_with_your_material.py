import streamlit as st
import time, pinecone, json, re
from openai import OpenAI
import google.generativeai as genai
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpointEmbeddings
from langchain_pinecone import PineconeVectorStore
from uuid import uuid4
from home.TestTopic.Pdf import generate_quiz_zip

pinecone_api_key = "pcsk_ffUJz_7hkW8pZMvpf99EXNU1y65SehYwa2nPKSbrtC8SCZX3mqUGPeYahH6gXpae1SNY6"  # Shivam's Api Key For Vector Store
pinecone_environment = "us-east-1"
pinecone_index_name = "example-index"

pc = pinecone.Pinecone(api_key=pinecone_api_key)

model_id = "sentence-transformers/all-MiniLM-L6-v2"
hf_token = "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"  ## Shivam's Write API for HF

embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

prompt_RAG_text = ""

HF_API_KEY = "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"  ## Read API
API_KEY = "AIzaSyAFUFDlRGjxn_VEDn24vQ1BeFnXuoc-SIM"  ## Gemini API
openai = OpenAI(api_key=HF_API_KEY, base_url="https://api-inference.huggingface.co/v1")
genai.configure(api_key=API_KEY)


def extract_json(response_text):
    try:
        return json.loads(re.sub(r"```json|```|\\n", "", response_text).strip())
    except json.JSONDecodeError:
        return None


def fetch_questions(text_content, quiz_level, number, extracted_text):
    PROMPT = f"""
        Generate exactly {number+10} multiple-choice questions (MCQs) from the text below for the topic "{text_content}" at {quiz_level} difficulty.
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
        Ensure the "MCQS" contains exactly {number + 10} questions and nothing else.
        Here is the text:
        \n{extracted_text}\n
        please **DO NOT** include any extra explanations or text. Only return the JSON part as shown above. Make sure the response is valid JSON without any additional formatting or extra text.
    """

    try:
        model_name = "models/gemini-1.5-flash"
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(PROMPT)
        res = response.text
        cleaned_res = extract_json(res).get("MCQS", [])
        return cleaned_res[:number] if len(cleaned_res) > number else cleaned_res
    except BaseException as e:
        return print("API Error!" + str(e)), 399


def display_question():
    """Display all questions and options."""
    questions = st.session_state.quiz_data["questions"]  # Get all questions
    st.session_state.timer = True

    for q_index, question in enumerate(questions):
        if st.session_state.timer:
            st.subheader(f"Q{q_index + 1}: {question['Mcq']}")

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
    """Countdown Timer for Test"""
    if "time_remaining" in st.session_state.quiz_data:
        while st.session_state.quiz_data["time_remaining"] > 0:
            mins, secs = divmod(st.session_state.quiz_data["time_remaining"], 60)
            st.subheader(f"⏳ Time Remaining: {mins}:{secs:02d}")

            time.sleep(1)  # Wait for 1 second
            st.session_state.quiz_data["time_remaining"] -= 2
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
    st.header("Test Results:")

    questions = st.session_state.quiz_data["questions"]  # Get the list of questions

    with st.status("Your result Generating...", expanded=False) as status:
        for i, question in enumerate(questions):
            selected = st.session_state.quiz_data["selected_options"].get(
                i, "Not Answered"
            )
            correct = question["Options"].get(question["Correct_option"], "Unknown")

            st.write(f"**{i+1}**" + " :- " + f"**{question['Mcq']}**")
            st.write(f"Your Answer: {selected}")
            st.write(f"Correct Answer: {correct}")

            if selected == correct:
                marks += 1
    status.update(label="View Result!", state="complete", expanded=False)
    st.subheader(f"Final Score: {marks} / {len(questions)}")

    if st.button("new test"):
        # Reset the quiz state after submission
        st.session.quiz_data = {
        "questions": [],
        "selected_options": {},
        "time_remaining": 0,
        "submitted": True,
    }
        st.session["timer"] = False
        st.cache_data.clear()
            
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
    st.session["timer"] = False

    st.cache_data.clear()  # Clearing cached data


def submit_quiz():
    if st.button("Submit Test", key="Submit"):
        st.markdown("## Thank You for Completing the Test! 🎉")
        st.balloons()
        marks = 0
        st.header("Test Results:")

        questions = st.session_state.quiz_data["questions"]

        with st.status("Your result Generating...", expanded=False) as status:
            for i, question in enumerate(questions):
                selected = st.session_state.quiz_data["selected_options"].get(
                    i, "Not Answered"
                )
                correct = question["Options"].get(question["Correct_option"], "Unknown")

                st.write(f"**{i+1}**" + " :- " + f"**{question['Mcq']}**")
                st.write(f"Your Answer: {selected}")
                st.write(f"Correct Answer: {correct}")

                if selected == correct:
                    marks += 1
        status.update(label="View Result!", state="complete", expanded=False)
        st.subheader(f"Final Score: {marks} / {len(questions)}")
        st.markdown(
    """
    <style>
    [data-testid="stSidebar"] { display: block !important; }
    [data-testid="collapsedControl"] { display: block !important; }
    </style>
    """,
    unsafe_allow_html=True,
)
        if st.button("new test"):
            # Reset the quiz state after submission
            st.session.quiz_data = {
            "questions": [],
            "selected_options": {},
            "time_remaining": 0,
            "submitted": True,
        }
            st.session["timer"] = False
            st.cache_data.clear()
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


def ask_topic_for_test():
    embeddings = HuggingFaceEndpointEmbeddings(
        model=model_id, task="feature-extraction", huggingfacehub_api_token=hf_token
    )
    index = pc.Index(pinecone_index_name)
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)
    st.subheader("Test With Your Own Materials")

    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = {
            "questions": {},
            "submitted": False,
            "time_remaining": 0,
        }

    user_query = st.text_input(
        "Enter the topic names which you would like to practice :",
        help="Separated by comma if multiple like Arrays,String in Data structure",
    )
    quiz_level = st.selectbox(
        "Select Difficulty:",
        [
            "Easy",
            "Medium",
            "Hard",
            "Mix(Easy, Medium, Hard)",
            "Blooms Taxonomy Based(Remember, Understand, Apply)",
        ],
    )
    number = st.slider("Number of Questions:", 5, 30, 10, 5)
    duration = st.slider("Set Test Time (minutes):", 1, 30, 10)  # User sets the timer

    if st.button("Generate Test"):
        with st.spinner("Generating Test, Please wait..."):
            if user_query:
                results = vector_store.similarity_search(user_query, k=5)
                global prompt_RAG_text
                prompt_RAG_text = ""
                for res in results:
                    prompt_RAG_text += res.page_content

                while True:
                    st.session_state.quiz_data["questions"] = fetch_questions(
                        user_query, quiz_level, number, prompt_RAG_text
                    )
                    if st.session_state.quiz_data["questions"]:
                        break
                    else:
                        continue
                st.session_state.quiz_data["current_index"] = 0
                st.session_state.quiz_data["submitted"] = False
                st.session_state.quiz_data["selected_options"] = {}
                st.session_state.quiz_data["time_remaining"] = (
                    duration * 60
                )  # Convert minutes to seconds
            else:
                st.warning("Please enter a topic to generate a Test.")

            st.rerun()


def test_with_your_material_interface():
    if (
        st.session_state["uploaded_and_analyzed"]
        and not st.session_state.quiz_data["questions"]
    ):
        ask_topic_for_test()
        st.markdown(
    """
    <style>
    [data-testid="stSidebar"] { display: block !important; }
    [data-testid="collapsedControl"] { display: block !important; }
    </style>
    """,
    unsafe_allow_html=True,
)
    elif (
        st.session_state["uploaded_and_analyzed"]
        and st.session_state.quiz_data["questions"]
    ):
        st.warning(
            "⚠️ Complete your Test and submit it in given time, Timer is shown below the Test..."
        )
        st.markdown(
    """
    <style>
    [data-testid="stSidebar"] { display: none; }
    [data-testid="collapsedControl"] { display: none; }
    </style>
    """,
    unsafe_allow_html=True,
)
    else:
        st.warning(
            "⚠️ If you not uploaded your Material please go to the upload material section first."
        )

    if st.session_state.quiz_data["questions"] and not st.session_state.quiz_data.get(
        "submitted", False
    ):
        display_question()
        st.markdown(
    """
    <style>
    [data-testid="stSidebar"] { display: none; }
    [data-testid="collapsedControl"] { display: none; }
    </style>
    """,
    unsafe_allow_html=True,
)
