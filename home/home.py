import streamlit as st
from streamlit_option_menu import option_menu

from home.LearnTopic.learn_particular_topic import learn_particular_topic_interface
from home.TestTopic.test_with_topic import test_with_topic_interface
from home.YourMaterialTopic.test_with_your_material import test_with_your_material_interface
from home.OMRCecking.omr_checking import omr_checking_interface
from home.UsageGuide.usage_guide import usage_guide_interface
from home.SamplePdf.sample_pdf_interface import download_omr_interface 
from home.MaterialUploader.upload_material import material_uploader_interface

def home():
    st.title("Welcome to AI-PrepMaster")
    
    st.sidebar.markdown(
        f"""
        <h1 style="font-size: 35px">Welcome, <strong>{st.session_state['username']}</h1>
        """,
        unsafe_allow_html = True
    )
    
    
    with st.sidebar:
        choice = option_menu(
            menu_title="Functionalities",
            options=['Learn particular topic', 'Test with topics',
                    'Test with your own material','Upload Your Material','OMR checking','Download OMR','Usage Guide'],
            menu_icon='none',
            default_index=6,
            styles={
                "container": {"padding": "5!important","background-color":'black'},
    "icon": {"color": "white", "font-size": "23px"}, 
    "nav-link": {"color":"white","font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "gray"},
    "nav-link-selected": {"background-color": "#02ab21"},}
        )


        
    if choice == "Learn particular topic":
        learn_particular_topic_interface()
        
    elif choice == "Test with topics":
        test_with_topic_interface()
        
    elif choice == "Test with your own material":
        test_with_your_material_interface()
        
    elif choice == "Upload Your Material":
        material_uploader_interface()
        
    elif choice == "OMR checking":
        omr_checking_interface()
        
    elif choice == "Usage Guide":
        usage_guide_interface()
    
    elif choice == "Download OMR":
        download_omr_interface()
    
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state.pop("username", None)
        st.session_state["page"] = "Login"
        st.session_state['uploaded_and_analyzed'] = False
        st.rerun()
