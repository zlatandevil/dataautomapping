import time
import streamlit as st
from models.sumUp import sumup
from models.dataMapping import scenario1 as sc1
# from models.dataMapping import upload_to_gemini, wait_for_files_active

path = "/Users/huyenvu/Documents/temp/gemini_apps/data_automapping/dataautomapping"
st.set_page_config(
    page_title="FuHoo Brothers",
    page_icon=f"{path}/images/icon.png",
    layout="wide",
)

col1, col2 = st.columns([8, 1])
st.sidebar.image(f"{path}/images/icon.png")
st.sidebar.markdown("""
    **Greetings, my FuHo brother!**

    I'm your trusty Data Mapping AI assistant, here to help you through the intricate world of data transformation.
    """
)

with col1:
    st.title("Mapping Automation")
    # st.image(f"{path}/images/icon.png")

def scen2(brd):
    init = sc1()
    reply = init.send_message(f'DMP2 {brd}')
    st.markdown(reply.text)

def scen1():
    uploaded_file = st.file_uploader("Browse")
    # Check availability
    if uploaded_file is not None:
        # Enable the button if a file is uploaded
        if st.button("Summarize information in BRD"):
            brd = (uploaded_file.read())
            st.markdown(sumup(brd))
            if st.button('Check Data Availability'):
                st.empty()
                scen2(brd)
                
    else:
        # Show a disabled button if no file is uploaded
        st.button("Summarize information in BRD", disabled=True)
        st.write("Please upload a file to enable the button.")




scen1()
