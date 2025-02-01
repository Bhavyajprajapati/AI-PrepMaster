import streamlit as st
from streamlit_option_menu import option_menu

# files imports
# here folders(LearnTopic,..) are in same module home then also we have to import it like home.LearnTopic
# because program is running like it is in our app.py
from home.LearnTopic.learn_particular_topic import learn_particular_topic_interface
from home.TestTopic.test_with_topic import test_with_topic_interface
from home.YourMaterialTopic.test_with_your_material import test_with_your_material_interface

def home():
    st.title("Welcome to AI-PrepMaster")
    
    # st.sidebar.image("media_files/icon.png",width=60)
    st.sidebar.markdown(
        f"""
        <h1 style="font-size: 35px">Welocme, <strong>{st.session_state['username']}</h1>
        """,
        unsafe_allow_html = True
    )
    
    

    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state.pop("username", None)
        st.session_state["page"] = "Login"
        st.rerun()

    with st.sidebar:
        choice = option_menu(
            menu_title="Functionalities",
            options=['Learn particular Topic', 'Test with Topics',
                     'Test with your own material'],
            # icons=['person-circle',]
            menu_icon='none',
            default_index=0,
            styles={
                "container": {"padding": "5!important","background-color":'black'},
    "icon": {"color": "white", "font-size": "23px"}, 
    "nav-link": {"color":"white","font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "gray"},
    "nav-link-selected": {"background-color": "#02ab21"},}
        )


        
    if choice == "Learn particular Topic":
        learn_particular_topic_interface()
        
    elif choice == "Test with Topics":
        test_with_topic_interface()
        
    elif choice == "Test with your own material":
        test_with_your_material_interface()
        

        
