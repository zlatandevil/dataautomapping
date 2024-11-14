import time
import streamlit as st
from models.sumUp import sumup
from models.dataMapping import scenario1 as sc1

class DataMappingApp:
    def __init__(self):
        self.path = "/Users/huyenvu/Documents/temp/gemini_apps/data_automapping/dataautomapping"
        self.setup_page_config()
        self.create_layout()
        init = sc1()
        st.write('Connected to AutoMapping.')
        st.write(init.send_message('Hello').text)
        
    def setup_page_config(self):
        st.set_page_config(
            page_title="FuHoo Brothers",
            page_icon=f"{self.path}/images/icon.png",
            layout="wide",
        )
        
    def create_layout(self):
        self.col1, self.col2 = st.columns([8, 1])
        self.setup_sidebar()
        self.setup_main_content()
        
    def setup_sidebar(self):
        st.sidebar.image(f"{self.path}/images/icon.png")
        st.sidebar.markdown("""
            **Greetings, my FuHo brother!**

            I'm your trusty Data Mapping AI assistant, here to help you through the intricate world of data transformation.
            """
        )
        
    def setup_main_content(self):
        with self.col1:
            st.title("Mapping Automation")
            
    def handle_scenario2(self, brd):

        reply = init.send_message(f'DMP2 {brd}')
        st.markdown(reply.text)
        
    def handle_scenario1(self):
        uploaded_file = st.file_uploader("Browse")
        
        if uploaded_file is not None:
            if st.button("Summarize information in BRD"):
                brd = uploaded_file.read()
                st.markdown(sumup(brd))
                
                if st.button('Check Data Availability'):
                    # st.empty()
                    self.handle_scenario2(brd)
        else:
            st.button("Summarize information in BRD", disabled=True)
            st.write("Please upload a file to enable the button.")
            
    def run(self):
        self.handle_scenario1()


app = DataMappingApp()
app.run()