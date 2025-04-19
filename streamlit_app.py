import streamlit as st
from openai import OpenAI
import json
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="College Applications Assistant",
    page_icon="🎓",
    layout="wide"
)

# Initialize session state
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for User Information
with st.sidebar:
    st.title("🎓 College Applications Assistant")
    st.write("Please fill in your information to get personalized assistance.")
    
    # Personal Information
    st.header("Personal Information")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    
    # Academic Information
    st.header("Academic Information")
    gpa = st.number_input("GPA (out of 4.0)", min_value=0.0, max_value=4.0, step=0.01)
    sat_score = st.number_input("SAT Score (if applicable)", min_value=400, max_value=1600, step=10)
    act_score = st.number_input("ACT Score (if applicable)", min_value=1, max_value=36, step=1)
    
    # Target Universities
    st.header("Target Universities")
    universities = st.multiselect(
        "Select your target universities",
        ["Harvard", "Stanford", "MIT", "Yale", "Princeton", "Columbia", "Other"]
    )
    
    # Intended Major
    st.header("Academic Interests")
    major = st.text_input("Intended Major")
    career_goals = st.text_area("Career Goals")
    
    # Save Profile Button
    if st.button("Save Profile"):
        st.session_state.user_profile = {
            "name": name,
            "email": email,
            "phone": phone,
            "gpa": gpa,
            "sat_score": sat_score,
            "act_score": act_score,
            "universities": universities,
            "major": major,
            "career_goals": career_goals
        }
        st.success("Profile saved successfully!")

# Main Chat Interface
st.title("College Applications Assistant")
st.write("I'm here to help you with your college applications. Ask me anything about essays, applications, or interview preparation!")

# Initialize OpenAI client
openai_api_key = st.secrets["openai_api_key"]
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like help with?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare context for the AI
        context = f"""
        User Profile:
        {json.dumps(st.session_state.user_profile, indent=2)}
        
        Current Chat History:
        {json.dumps(st.session_state.messages, indent=2)}
        """

        # Generate response
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are a college applications assistant. 
                Your role is to help students with their college applications, including:
                - Essay writing and review
                - Application strategy
                - Interview preparation
                - University-specific guidance
                - Timeline management
                
                Be supportive, constructive, and provide specific, actionable advice."""},
                {"role": "user", "content": f"Context: {context}\n\nUser Question: {prompt}"}
            ],
            stream=True,
        )

        # Display assistant's response
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
