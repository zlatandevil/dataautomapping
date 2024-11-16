import time
import streamlit as st
import google.generativeai as genai
genai.configure(api_key='AIzaSyBHOARN4j3c-yDp3DjhHjHT04JYLqZSBZY')
def sumup(brd):
    model = genai.GenerativeModel("gemini-1.5-flash")
    reply = model.generate_content(f"""
        Sum up information in this Business Requirement Declaration 
        //"{brd}"//
        And list down all features this BRD look need to identify!
        Beautify your return in markdown as much as possible. At least beautify your list of features!
        Shorten your answer in 300 words and return information in suitable table format.
        """)
    return reply.text
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

def scen1():
    uploaded_file = st.file_uploader("Browse")
    # Check availability
    if uploaded_file is not None:
        # Enable the button if a file is uploaded
        brd = (uploaded_file.read())
        st.markdown(sumup(brd))
        #st.markdown(summary_text)

    else:
        # Show a disabled button if no file is uploaded
        st.button("Sum Up", disabled=True)
        st.write("Please upload a file to enable the button.")

def scen2(brd):
    return False


scen1()
