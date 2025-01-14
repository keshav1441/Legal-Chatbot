import streamlit as st

# Set the page configuration
st.set_page_config(
    page_title="Basic Streamlit App",
    page_icon="✨",
    layout="centered"
)

# Main function
def main():
    st.title("Welcome to Streamlit! ✨")
    st.write("This is a basic Streamlit application to get you started.")
    
    # Input text
    user_input = st.text_input("What's your name?", placeholder="Enter your name here...")
    
    # Display user input
    if user_input:
        st.write(f"Hello, {user_input}! 👋")
    
    # Checkbox example
    if st.checkbox("Show an inspirational quote"):
        st.write("🌟 *The best way to predict the future is to create it.* – Peter Drucker")
    
    # Slider example
    number = st.slider("Pick a number", min_value=0, max_value=100, value=50)
    st.write(f"You picked: {number}")
    
    # Button example
    if st.button("Click me!"):
        st.success("You clicked the button!")
    
    # File uploader example
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "csv"])
    if uploaded_file:
        st.write("Uploaded file content:")
        st.text(uploaded_file.read().decode("utf-8"))

if __name__ == "__main__":
    main()
