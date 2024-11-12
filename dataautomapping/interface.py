import streamlit as st
from models.talkwithGemini import chatbot
from models.dataMapping import mapping

st.set_page_config(
    page_title="SQL Talk with BigQuery",
    # page_icon="vertex-ai.png",
    layout="wide",
)

col1, col2 = st.columns([8, 1])
with col1:
    st.title("SQL Talk with BigQuery")
with col2:
    st.write("SQL Talk with BigQuery")
    #st.image("vertex-ai.png")

st.subheader("Powered by Function Calling in Gemini")
user_input = st.text_input("Enter your requirement:") #, placeholder="Your name here")
if user_input:
    uppercase_text = mapping(user_input)
    st.markdown(uppercase_text)

# st.markdown(
#     "[Source Code](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gemini/function-calling/sql-talk-app/)   •   [Documentation](https://cloud.google.com/vertex-ai/docs/generative-ai/multimodal/function-calling)   •   [Codelab](https://codelabs.developers.google.com/codelabs/gemini-function-calling)   •   [Sample Notebook](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/function-calling/intro_function_calling.ipynb)"
# )
