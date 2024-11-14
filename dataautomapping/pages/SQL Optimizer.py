import streamlit as st
import google.generativeai as genai

def init_model():
    genai.configure(api_key="AIzaSyCn9L6fMD6ORt0b21mmVXBH0lQnFaYH7i8")
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model

def sql_optimize(input_str):
    # Assuming you already have this function implemented
    # This is just a placeholder - replace with your actual BB function
    model = init_model()
    reply = model.generate_content(f"Optimize this SQL syntax: {input_str}") 
    return reply.text

def main(title_ = 'SQL Optimizer',
         ):
    st.title(title_)
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'editing' not in st.session_state:
        st.session_state.editing = {}

    # Chat input
    user_input = st.chat_input("Enter your message (type 'end' to stop)")

    if user_input:
        if user_input.lower() == 'end':
            st.write("Chat ended. Refresh to start a new chat.")
        else:
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": user_input})
            # Process with BB function and add response
            response = sql_optimize(user_input)
            markdown_response = f"""{response}"""
            st.session_state.messages.append({"role": "assistant", "content": markdown_response})

    # Display chat history with edit functionality
    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                col1, col2 = st.columns([0.95, 0.05])
                with col1:
                    if idx in st.session_state.editing and st.session_state.editing[idx]:
                        edited_response = st.text_area(
                            "Edit response",
                            value=message["content"],
                            key=f"edit_{idx}",
                            label_visibility="collapsed"
                        )
                        if st.button("Save", key=f"save_{idx}", type="primary"):
                            st.session_state.messages[idx]["content"] = edited_response
                            st.session_state.editing[idx] = False
                            st.rerun()
                    else:
                        st.markdown(message["content"])
                with col2:
                    if st.button("✏️", key=f"edit_btn_{idx}"):
                        st.session_state.editing[idx] = not st.session_state.editing.get(idx, False)
                        st.rerun()
            else:
                st.write(message["content"])

    # Add clear button
    if st.button("Clear Chat 🗑️"):
        st.session_state.messages = []
        st.session_state.editing = {}
        st.rerun()

main()