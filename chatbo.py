import streamlit as st
from dotenv import load_dotenv
import os
from groq import Groq

# Load environment variables
load_dotenv()

# Setup Groq client
def setup_groq_client(api_key):
    return Groq(api_key=api_key)

# Fetch AI response
def fetch_ai_response(client, conversation_history):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation_history
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error communicating with Groq API: {str(e)}")
        return None

# Initialize session state
def initialize_session_state():
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = [
            {"role": "system", "content": "You are a legal chatbot."},
            {"role": "assistant", "content": "Hello! I am here to assist you with legal queries. How can I help?"}
        ]
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

# Display chat history
def display_chat_history():
    st.markdown('<div style="max-height: 70vh; overflow-y: auto; padding: 10px; background-color: #f9f9f9; border-radius: 10px;">', unsafe_allow_html=True)
    for message in st.session_state.conversation_history:
        if message["role"] == "user":
            st.markdown(f'<div style="text-align: right; background-color: #cfe2f3; color: #333; padding: 10px; margin: 5px; border-radius: 10px;">You: {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="text-align: left; background-color: #d9ead3; color: #333; padding: 10px; margin: 5px; border-radius: 10px;">AI: {message["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Handle user input
def handle_user_input(client):
    if st.session_state.user_input:
        user_message = st.session_state.user_input
        st.session_state.conversation_history.append({"role": "user", "content": user_message})
        with st.spinner("AI is thinking..."):
            ai_response = fetch_ai_response(client, st.session_state.conversation_history)
        if ai_response:
            st.session_state.conversation_history.append({"role": "assistant", "content": ai_response})
        st.session_state.user_input = ""

# Main app
def main():
    st.set_page_config(page_title="Legal Chatbot", page_icon="💬")
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("API key is missing. Please set the 'GROQ_API_KEY' in your .env file.")
        return
    client = setup_groq_client(api_key)
    initialize_session_state()
    st.title("Legal Chatbot 💬")
    display_chat_history()
    st.text_input("", key="user_input", on_change=handle_user_input, args=(client,), placeholder="Type your message...")

if __name__ == "__main__":
    main()
