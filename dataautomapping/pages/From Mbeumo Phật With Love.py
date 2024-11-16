import streamlit as st

def main():
    # Initial markdown input
    initial_markdown = "This is some **bold** text and *italic* text."

    # Text area for editing
    edited_markdown = st.text_area("Edit Markdown", value=initial_markdown, height=200)

    # Button to re-render
    if st.button("Render Markdown"):
        st.empty()
        st.markdown(edited_markdown)
main()