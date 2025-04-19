import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("🎓 College Application Assistant")
st.write(
    "Welcome to your personal college application assistant! I can help you with:"
    "\n- Writing and reviewing college essays"
    "\n- Preparing for interviews"
    "\n- Understanding application requirements"
    "\n- Creating a strong application strategy"
    "\n- Answering questions about the college application process"
)

# Initialize the OpenAI client
openai_api_key = st.secrets["OPENAI_API_KEY"]
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": """You are an expert college application advisor with years of experience helping students get into top universities. 
                Your role is to provide personalized guidance on college applications, essays, interviews, and the overall application process.
                Be supportive, encouraging, and provide specific, actionable advice. 
                When reviewing essays or materials, offer constructive feedback while maintaining a positive tone.
                Always consider the student's unique background and goals in your responses."""
            }
        ]

    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] != "system":  # Don't display system messages
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("How can I help with your college application?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            stream=True,
        )

        # Display assistant response
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
