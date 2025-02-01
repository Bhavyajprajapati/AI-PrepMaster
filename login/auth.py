import streamlit as st
from login.database import users_collection
from login.utils import hash_password, verify_password

def signup(email, username, password, favorite_person):
    if users_collection.find_one({"email": email}):
        return "Email already exists. Please use another."
    
    hashed_password = hash_password(password)
    users_collection.insert_one({
        "email": email,
        "username": username,
        "password": hashed_password,
        "favorite_person": favorite_person.lower()
    })
    return "Signup successful! You can now log in."

def login(email, password):
    user = users_collection.find_one({"email": email})
    if user and verify_password(password, user["password"]):
        return user["username"]
    return None

def reset_password(email, favorite_person, new_password):
    user = users_collection.find_one({"email": email})
    if not user:
        return "Email not found!"
    
    if user["favorite_person"] == favorite_person.lower():
        hashed_password = hash_password(new_password)
        users_collection.update_one({"email": email}, {"$set": {"password": hashed_password}})
        return "Password reset successful! You can now log in."
    else:
        return "Incorrect security answer!"

def login_st_interface():
    st.markdown("""
        <h3 style='text-align:center;'>Ai-PreapMaster</h3>            
        """,unsafe_allow_html=True)
    st.image("media_files/home_img.png",use_column_width=True)
    st.markdown("""
        <p style='font-size:18px; text-align:center'>
        Want to learn, why wait? just login and <strong style='color:dodgerblue'>Get Started!<strong></p>
        """,unsafe_allow_html=True)
    
    st.subheader("Login to Your Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        username = login(email, password)
        if username:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["page"] = "Home"
            st.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.error("Invalid email or password.")

def signup_st_interface():
    st.subheader("Create a New Account")
    email = st.text_input("Email")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    favorite_person = st.text_input("Who is your Favorite Person? (Used for password reset)")

    if st.button("Submit"):
        if email and new_username and new_password and favorite_person:
            message = signup(email, new_username, new_password, favorite_person)
            if "successful" in message:
                st.success(message)
            else:
                st.error(message)
        else:
            st.warning("Please fill in all fields.")

def forget_st_interface():
    st.subheader("Reset Your Password")
    email = st.text_input("Enter your registered Email")
    favorite_person = st.text_input("Who is your Favorite Person?")
    new_password = st.text_input("Enter New Password", type="password")

    if st.button("Reset Password"):
        if email and favorite_person and new_password:
            message = reset_password(email, favorite_person, new_password)
            if "successful" in message:
                st.success(message)
            else:
                st.error(message)
        else:
            st.warning("Please fill in all fields.")
