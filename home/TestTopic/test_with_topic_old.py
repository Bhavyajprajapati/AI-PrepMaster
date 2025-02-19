import streamlit as st
import json
import time
import re
import google.generativeai as genai
from home.TestTopic.Pdf import generate_quiz_zip

session = st.session_state
API_KEY = "AIzaSyAFUFDlRGjxn_VEDn24vQ1BeFnXuoc-SIM"
genai.configure(api_key=API_KEY)


def extract_json(response_text):
    try:
        return json.loads(re.sub(r"```json|```|\\n", "", response_text).strip())
    except json.JSONDecodeError:
        return None


def fetch_questions(text_content, quiz_level, number):
    PROMPT = f"""
        Extract {number + 10} of  MCQs from the following text :\n{text_content}\n
        for level {quiz_level} also
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
    message = [{"role": "user", "content": PROMPT}]

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
    questions = session.quiz_data["questions"]  # Get all questions
    session.timer = True

    for q_index, question in enumerate(questions):
        if session.timer:
            st.subheader(f"Q{q_index + 1}: {question['Mcq']}")

            # Display radio button for options
            selected_option = st.radio(
                f"Select an answer :",
                options=list(question["Options"].values()),  # Extract values only
                key=f"q_{q_index}",  # Unique key per question
                index=None,  # Allow user to choose, but no default selection
            )
            # Store the selected answer
            session.quiz_data["selected_options"][q_index] = selected_option

    submit_quiz()
    countdown_timer()


def countdown_timer():
    """Countdown Timer for Test"""
    if "time_remaining" in session.quiz_data:
        while session.quiz_data["time_remaining"] > 0:
            mins, secs = divmod(session.quiz_data["time_remaining"], 60)
            st.subheader(f"⏳ Time Remaining: {mins}:{secs:02d}")

            time.sleep(1)  # Wait for 1 second
            session.quiz_data["time_remaining"] -= 2
            st.rerun()  # Rerun Streamlit app to update timer

        # Auto-submit the quiz when time is up
        if not st.session_state.quiz_data["submitted"]:
            auto_submit_quiz()


def auto_submit_quiz():
    """Automatically submits the quiz when the timer runs out"""
    session.quiz_data["submitted"] = True
    session.quiz_data["time_remaining"] = 0  # Reset Time

    # Show thank you message
    st.markdown("## Thank You for Completing the Quiz! 🎉")
    st.balloons()
    marks = 0
    st.header("Test Results:")

    questions = session.quiz_data["questions"]

    with st.status("Your result Generating...", expanded=False) as status:
        for i, question in enumerate(questions):
            selected = session.quiz_data["selected_options"].get(i, "Not Answered")
            correct = question["Options"].get(question["Correct_option"], "Unknown")

            st.write(f"**{i+1}**" + " :- " + f"**{question['Mcq']}**")
            st.write(f"Your Answer: {selected}")
            st.write(f"Correct Answer: {correct}")

            if selected == correct:
                marks += 1

    status.update(label="View Result!", state="complete", expanded=False)
    st.subheader(f"Final Score: {marks} / {len(questions)}")

    try:
        # Generate ZIP file containing both PDFs
        zip_buffer = generate_quiz_zip(session.quiz_data)

        # Download button for ZIP file
        st.download_button(
            label="Download Test Files",
            data=zip_buffer,
            file_name="test_files.zip",
            mime="application/zip",
        )

    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")

    # Reset the quiz state after submission
    session.quiz_data = {
        "questions": [],
        "selected_options": {},
        "time_remaining": 0,
        "submitted": True,
    }
    session["timer"] = False
    st.cache_data.clear()


def submit_quiz():
    if st.button("Submit Test", key="Submit"):
        st.markdown("## Thank You for Completing the Quiz! 🎉")
        st.balloons()
        marks = 0
        st.header("Test Results:")

        questions = session.quiz_data["questions"]

        with st.status("Your result Generating...", expanded=False) as status:
            for i, question in enumerate(questions):
                selected = session.quiz_data["selected_options"].get(i, "Not Answered")
                correct = question["Options"].get(question["Correct_option"], "Unknown")

                st.write(f"**{i+1}**" + " :- " + f"**{question['Mcq']}**")
                st.write(f"Your Answer: {selected}")
                st.write(f"Correct Answer: {correct}")

                if selected == correct:
                    marks += 1

        status.update(label="View Result!", state="complete", expanded=False)
        st.subheader(f"Final Score: {marks} / {len(questions)}")

        try:
            # Generate ZIP file containing both PDFs
            zip_buffer = generate_quiz_zip(session.quiz_data)

            # Download button for ZIP file
            st.download_button(
                label="Download Test Files",
                data=zip_buffer,
                file_name="test_files.zip",
                mime="application/zip",
            )

        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")

        # Reset the quiz state after submission
        session.quiz_data = {
            "questions": [],
            "selected_options": {},
            "time_remaining": 0,
            "submitted": True,
        }
        session["timer"] = False
        st.cache_data.clear()


def test_with_topic_interface():
    st.subheader("Test With Topics")
    # Initialize session state for the quiz
    if "quiz_data" not in session:
        session.quiz_data = {
            "questions": {},
            "submitted": False,
            "time_remaining": 0,
            "timer": False,
        }

    text_content = st.text_input(
        "Enter Topics for Test:",
        help="Seperated by comma if multiple like Arrays,String in Data structure",
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
        if not text_content:
            st.warning("⚠️ Please enter at least one topic before generating the test.")
        elif session.quiz_data["questions"] and not session.quiz_data["submitted"]:
            st.warning(
                "⚠️ You have an active test. Complete and submit it before starting a new one."
            )
        else:
            while True:
                session.quiz_data["questions"] = fetch_questions(
                    text_content, quiz_level, number
                )
                if st.session_state.quiz_data["questions"]:
                    break
                else:
                    continue
            session.quiz_data["selected_options"] = {}
            session.quiz_data["time_remaining"] = (
                duration * 60
            )  # Convert minutes to seconds

    if session.quiz_data["questions"] and not session.quiz_data.get("submitted", False):
        display_question()