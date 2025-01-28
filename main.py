import streamlit as st

st.set_page_config(
    page_title="AI-PrepMaster",
    page_icon="media_files/icon.png",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help':'mailto:shivam.bhundiya5403@gmail.com',
        'Report a bug':'mailto:shivam.bhundiya5403@gmail.com',
        'About':'''AI-PrepMaster is a Online Quick Exam Preparation System which helps students for their
                exam very quickly using Letest AI and with their own material also.
                It also provides Result eveluation metrics, and suggestions for topic to learn more.'''
    }
)

st.write("Hello Friends...")

choise = st.sidebar.selectbox('Select your way to prepare.',('Prepare with topics','Prepare with own material'),index=None,placeholder="Select Here...")