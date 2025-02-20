import streamlit as st
from pymongo import MongoClient
import datetime

# MongoDB connection


# Streamlit app
def user_feedback_interface():
    client = MongoClient("mongodb+srv://sumitraval120:lCMRq8Ni6I3PlxBE@clusterforai.otg78.mongodb.net/")
    db = client["feedback_db"]
    collection = db["feedbacks"]
    # st.set_page_config(page_title="Feedback Collection", page_icon=":speech_balloon:", layout="wide")

    # Custom CSS for animations and styling
    st.markdown("""
    <style>
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    .fadeIn {
        animation: fadeIn 2s;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        padding: 10px 24px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("We Value Your Feedback! 🌟")
    st.markdown("""
    <div class="fadeIn">
        <h3>Your opinion matters to us! Please take a moment to share your experience.</h3>
    </div>
    """, unsafe_allow_html=True)

    # Feedback form
    with st.form("feedback_form"):
        name = st.text_input("Your Name (Optional)")
        email = st.text_input("Your Email (Optional)")
        feedback = st.text_area("Your Feedback", placeholder="Share your thoughts here...")
        rating = st.slider("Rate your experience", 1, 5, 3)
        submitted = st.form_submit_button("Submit Feedback")

        if submitted:
            if feedback.strip() == "":
                st.error("Please provide some feedback before submitting.")
            else:
                # Create a feedback document
                feedback_doc = {
                    "name": name,
                    "email": email,
                    "feedback": feedback,
                    "rating": rating,
                    "timestamp": datetime.datetime.now()
                }
                # Insert into MongoDB
                collection.insert_one(feedback_doc)
                st.success("Thank you for your feedback! 💖")
                st.balloons()

    # Additional attractive elements
    st.markdown("""
    <div class="fadeIn">
        <h3>Why Your Feedback Matters:</h3>
        <ul>
            <li>Helps us improve our services</li>
            <li>Guides future updates and features</li>
            <li>Ensures we meet your expectations</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="fadeIn">
        <h3>Thank you for being a part of our journey! 🚀</h3>
    </div>
    """, unsafe_allow_html=True)
