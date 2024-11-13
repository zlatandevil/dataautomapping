import time
import streamlit as st
from models.dataMapping import scenario1 as sc1
from models.dataMapping import upload_to_gemini, wait_for_files_active
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

files = [
  upload_to_gemini(f"{path}/docs/idv_des.csv", mime_type="text/csv"),
  upload_to_gemini(f"{path}/docs/idv.csv", mime_type="text/csv"),
  upload_to_gemini(f"{path}/docs/org_des.csv", mime_type="text/csv"),
]

# Some files have a processing delay. Wait for them to be ready.
wait_for_files_active(files)

aa = sc1(files)

# Connect Confluence to Publish