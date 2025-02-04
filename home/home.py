import streamlit as st
from streamlit_option_menu import option_menu

# files imports
# here folders(LearnTopic,..) are in same module home then also we have to import it like home.LearnTopic
# because program is running like it is in our app.py
from home.LearnTopic.learn_particular_topic import learn_particular_topic_interface
from home.TestTopic.test_with_topic import test_with_topic_interface
from home.YourMaterialTopic.test_with_your_material import test_with_your_material_interface
from home.OMRCecking.omr_checking import omr_checking_interface
from home.TestForOMR.test_for_omr import test_create_for_omr_purpose_interface
from home.UsageGuide.usage_guide import usage_guide_interface

def home():
    st.title("Welcome to AI-PrepMaster")
    
    # st.sidebar.image("media_files/icon.png",width=60)
    st.sidebar.markdown(
        f"""
        <h1 style="font-size: 35px">Welocme, <strong>{st.session_state['username']}</h1>
        """,
        unsafe_allow_html = True
    )
    
    
    with st.sidebar:
        choice = option_menu(
            menu_title="Functionalities",
            options=['Learn particular topic', 'Test with topics',
                     'Test with your own material','Create test for OMR purpose','OMR checking','Usage Guide'],
            # icons=['person-circle',]
            menu_icon='none',
            default_index=5,
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
        
    elif choice == "Create test for OMR purpose":
        test_create_for_omr_purpose_interface()
        
    elif choice == "OMR checking":
        omr_checking_interface()
        
    elif choice == "Usage Guide":
        usage_guide_interface()
        
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state.pop("username", None)
        st.session_state["page"] = "Login"
        st.session_state['uploaded_and_analyzed'] = False
        st.rerun()

        
