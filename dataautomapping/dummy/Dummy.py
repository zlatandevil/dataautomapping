import time
import streamlit as st
# from models.dataMapping import scenario1 as sc1
# from models.dataMapping import upload_to_gemini, wait_for_files_active
from models import talkwithGemini as sql_

def read_uploaded_file(uploaded_file):
  """Reads the contents of an uploaded file.

  Args:
    uploaded_file: The uploaded file object.

  Returns:
    The contents of the file as a string.
  """

  if uploaded_file is not None:
    # Read the contents of the uploaded file
    contents = uploaded_file.read().decode('utf-8')
    return contents
  else:
    return None

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
            contents = uploaded_file.read().decode('utf-8')
            st.write(contents)

    else:
        # Show a disabled button if no file is uploaded
        st.button("Check Availability", disabled=True)
        st.write("Please upload a file to enable the button.")
    
    if uploaded_file is not None:
    # Read the contents of the uploaded file