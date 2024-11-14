import time
import streamlit as st
# from models.dataMapping import scenario1 as sc1
# from models.dataMapping import upload_to_gemini, wait_for_files_active
from models import talkwithGemini as sql_

path = "/Users/huyenvu/Documents/temp/gemini_apps/data_automapping/dataautomapping"
st.set_page_config(
    page_title="SQL Talk with BigQuery",
    page_icon=f"{path}/images/icon.png",
    layout="wide",
)

col1, col2 = st.columns([8, 1])
st.sidebar.image(f"{path}/images/icon.png")
st.sidebar.markdown("""
    **Greetings, my FuHo brother!**

    I'm your trusty Data Mapping AI assistant, here to guide you through the intricate world of data transformation.
    """
)

with col1:
    st.title("Mapping Automation")
    # st.image(f"{path}/images/icon.png")

with st.expander("Upload your BRD file to start!", False):
    uploaded_file = st.file_uploader("Browse")
# Check availability
    if uploaded_file is not None:
        # Enable the button if a file is uploaded
        if st.button("Check Availability"):
            st.write("Button clicked!")
    else:
        # Show a disabled button if no file is uploaded
        st.button("Check Availability", disabled=True)
        st.write("Please upload a file to enable the button.")

# Render Automapping


# # Some files have a processing delay. Wait for them to be ready.
# wait_for_files_active(files)

# aa = sc1(files)
def BB(x: str):
    return (x + 'aaa').upper()

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Input text box for user input


# # Process the input when the user presses Enter
# if user_input:

#     # Use the BB function to process the input
#     response = BB(user_input)
    
#     # Add the input and response to chat history
#     st.session_state.chat_history.append({"user": [user_input], "model": [response]})
#     st.write(response)
    
#     # Clear the input after processing
#     st.rerun()

st.title("Vietnamese Text Processor")
messages = []

def main():
    st.title("BB Chatbot")
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Chat input
    user_input = st.chat_input("Enter your message (type 'end' to stop)")

    if user_input:
        if user_input.lower() == 'end':
            st.write("Chat ended. Refresh to start a new chat.")
        else:
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": user_input})
            # Process with BB function and add response
            response = BB(user_input)
            st.session_state.messages.append({"role": "assistant", "content": response})

    # Display chat history with edit functionality
    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                # Make the assistant's response editable
                edited_response = st.text_area(
                    "Edit response",
                    value=message["content"],
                    key=f"edit_{idx}",
                    label_visibility="collapsed"
                )
                # Add update button
                if st.button("Update", key=f"update_{idx}"):
                    st.session_state.messages[idx]["content"] = edited_response
                    st.rerun()
            else:
                # Display user message normally
                st.write(message["content"])

    # Add clear button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()