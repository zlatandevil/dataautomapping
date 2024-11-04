import time

from google.cloud import bigquery
import streamlit as st
from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool

BIGQUERY_DATASET_ID = "thelook_ecommerce"
# model = GenerativeModel(
#     "gemini-1.5-pro",
#     generation_config={"temperature": 0},
#     tools=[sql_query_tool],
# )

st.set_page_config(
    page_title="FuHo Brothers",
    page_icon="mbeumo.avif",
    layout="wide",
)

col1, col2 = st.columns([8, 1])
with col1:
    st.title("SQL Talk with BigQuery")
with col2:
    st.image("mbeumo.avif")

st.subheader("Powered by Function Calling in Gemini")

st.markdown(
    "[Source Code](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gemini/function-calling/sql-talk-app/)   •   [Documentation](https://cloud.google.com/vertex-ai/docs/generative-ai/multimodal/function-calling)   •   [Codelab](https://codelabs.developers.google.com/codelabs/gemini-function-calling)   •   [Sample Notebook](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/function-calling/intro_function_calling.ipynb)"
)