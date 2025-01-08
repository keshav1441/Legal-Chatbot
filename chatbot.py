import streamlit as st
from prompt_utils import usecase_prompt
import os
from dotenv import load_dotenv
from groq import Groq # type: ignore

# Load environment variables from the .env file
load_dotenv()

# Function to initialize the Groq client
def setup_groq_client(api_key):
    return Groq(api_key=api_key)

# Function to fetch AI response from Groq
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

# Load custom CSS
def load_css():
    return """
                <style>
        /* Ensure full screen with no scroll */
        body {
            margin: 0;  /* Remove any default margin */
            padding: 0;  /* Remove any default padding */
            height: 100vh;  /* Full viewport height */
            background-color: #f4f6f9;  /* Light, soft background for a clean look */
            font-family: 'Arial', sans-serif;  /* Clean, modern font */
            display: flex;
            flex-direction: column;
        }

        /* Chat container that fills the screen with auto-scrolling and increased width */
        .chat-container {
            flex-grow: 1;  /* Takes up remaining space */
            overflow-y: auto;
            padding: 10px;
            border: 1px solid #e0e0e0;  /* Soft gray border for subtlety */
            border-radius: 10px;
            margin-bottom: 20px;
            box-sizing: border-box;  /* Ensures padding does not affect the scroll */
            display: flex;
            flex-direction: column;
            justify-content: flex-end;  /* Align messages to the bottom */
            max-width: 90vw; 
            margin-left: auto;  /* Center the chat container horizontally */
            margin-right: auto;
        }

        /* User message bubble styling */
        .chat-bubble-user {
            margin: 10px 0 10px auto;
            padding: 12px;
            border-radius: 15px;
            background-color: #757a7a;  /* Light gray for user messages */
            color: #eeeeee;  /* Light text for contrast */
            max-width: 70%;
            text-align: left;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);  /* Subtle shadow for depth */
        }

        /* AI message bubble styling */
        .chat-bubble-ai {
            margin: 10px 0;
            padding: 12px;
            border-radius: 15px;
            background-color: #4e6e5b;  /* Slightly darker green for AI messages */
            color: #eeeeee;  /* Light text for contrast */
            max-width: 70%;
            text-align: left;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);  /* Subtle shadow for depth */
        }

        /* Input field inside chat container */
        .chat-input-container {
            display: flex;
            justify-content: center;
            padding-top: 10px; /* To ensure some space between chat and input */
        }

        .stTextInput>div>div>input {
            border-radius: 20px;
            width: 90%;  /* Adjust width to fit inside the chat window */
        }

        /* Focus effect on input field */
        .stTextInput>div>div>input:focus {
            outline: none;  /* Remove default focus outline */
        }
        </style>

    """

# Function to initialize session state with a welcome message
def initialize_session_state():
    if "conversation_history" not in st.session_state:
        # Add initial greeting from the chatbot
        st.session_state.conversation_history = [
            {"role": "system", "content": usecase_prompt()},
            {"role": "assistant", "content": "Hello! I am your AI Assistant. How can I help you today?"}
        ]
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

# Function to display the chat history
def display_chat_history():
    chat_history = '<div class="chat-container">'
    for message in st.session_state.conversation_history:
        if message["role"] == "user":
            chat_history += f'<div class="chat-bubble-user">You :  {message["content"]}</div>'
        elif message["role"] == "assistant":
            chat_history += f'<div class="chat-bubble-ai">AI Assistant :  {message["content"]}</div>'
    chat_history += "</div>"
    st.markdown(chat_history, unsafe_allow_html=True)

# Function to handle user input
def handle_user_input(client):
    if st.session_state.user_input:
        user_message = st.session_state.user_input
        st.session_state.conversation_history.append(
            {"role": "user", "content": user_message}
        )
        
        with st.spinner("AI is thinking..."):
            ai_response = fetch_ai_response(client, st.session_state.conversation_history)
            
        if ai_response:
            st.session_state.conversation_history.append(
                {"role": "assistant", "content": ai_response}
            )
        
        # Clear the input after submitting
        st.session_state.user_input = ""

# Main function to run the app
def main():
    st.set_page_config(page_title="AI Chatbot", page_icon="💬")
    
    # Load API key
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        st.error("API key is missing. Please set the 'GROQ_API_KEY' in your .env file.")
        return
    
    # Initialize Groq client
    client = setup_groq_client(api_key)
    
    # Load custom CSS
    st.markdown(load_css(), unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # App title
    st.title("Legal Chatbot")
    
    # Display chat history
    display_chat_history()
    
    # Chat input
    st.text_input(
    "",  # Empty string removes the default text
    key="user_input",
    on_change=handle_user_input,
    args=(client,),
    placeholder="Type your message and press Enter..."
)

if __name__ == "__main__":
    main()
