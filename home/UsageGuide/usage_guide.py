import streamlit as st

def usage_guide_interface():
    if st.session_state["logged_in"]:
        st.subheader("How to use")
    
    usage = """
    <h4>
        <b>Select your interst from sidebar</b>
    </h4>
    
    """
    st.markdown(usage,unsafe_allow_html=True)
