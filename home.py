import streamlit as st
from streamlit_option_menu import option_menu

def home():
    st.title("Welcome to AI-PrepMaster")
    st.sidebar.write(f"Welcome, **{st.session_state['username']}**!")



    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state.pop("username", None)
        st.session_state["page"] = "Login"
        st.rerun()

    with st.sidebar:
        choice = option_menu(
            menu_title="Functionalities",
            options=['Prepare with topics', 'Prepare with own material'],
            # icons=['person-circle',]
            menu_icon='none',
            default_index=0,
            styles={
                "container": {"padding": "5!important","background-color":'black'},
    "icon": {"color": "white", "font-size": "23px"}, 
    "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
    "nav-link-selected": {"background-color": "#02ab21"},}
        )


    # if you want to set particular text to be show at some conditions you can use below code using empty()    
    # choice = st.sidebar.selectbox('Select your way to prepare.', ('Prepare with topics', 'Prepare with own material'), index=None, placeholder="Select Here...")
    # temp_text = st.empty()

    # temp_text.write("Please select your way to prepare from sidebar")
    if choice:
        st.subheader(choice)
        # temp_text.empty()
