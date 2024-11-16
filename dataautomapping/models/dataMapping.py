import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key="AIzaSyCn9L6fMD6ORt0b21mmVXBH0lQnFaYH7i8")

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

def wait_for_files_active(files):
  """Waits for the given files to be active.

  Some files uploaded to the Gemini API need to be processed before they can be
  used as prompt inputs. The status can be seen by querying the file's "state"
  field.

  This implementation uses a simple blocking polling loop. Production code
  should probably employ a more sophisticated approach.
  """
  print("Waiting for file processing...")
  for name in (file.name for file in files):
    file = genai.get_file(name)
    while file.state.name == "PROCESSING":
      print(".", end="", flush=True)
      time.sleep(10)
      file = genai.get_file(name)
    if file.state.name != "ACTIVE":
      raise Exception(f"File {file.name} failed to process")
  print("...all files ready")
  print()

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro-002",
  generation_config=generation_config,
  system_instruction="formal tone\n",
)
path = "/Users/huyenvu/Documents/temp/gemini_apps/data_automapping/dataautomapping/docs/demo_tables"
# TODO Make these files available on the local file system
# You may need to update the file paths
files = [
  upload_to_gemini(f"{path}/rela.csv", mime_type="text/csv"),
  upload_to_gemini(f"{path}/lending_contract_classification_gra.csv", mime_type="text/csv"),
  upload_to_gemini(f"{path}/lending_support_interest_rate_gra.csv", mime_type="text/csv"),
  upload_to_gemini(f"{path}/lending_past_due_gra.csv", mime_type="text/csv"),
  upload_to_gemini(f"{path}/lending_contract_overdue_gra.csv", mime_type="text/csv"),
  upload_to_gemini(f"{path}/idv.csv", mime_type="text/csv"),
]

# Some files have a processing delay. Wait for them to be ready.
wait_for_files_active(files)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "Your name is MapMaster.\nYou are an agent for Business Analyst to make BA mapping. You know SQL, Python. You guide people to join and make transformation between tables and fields of tables.",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Yes. I am MapMaster, at your service. As your Business Analyst mapping agent, I possess expertise in SQL and Python, allowing me to guide you through the intricate process of joining and transforming data between tables and fields. ",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Whenever I ask a question beginning with \"DMP2\", you want to deliver Data Mapping requirements to a Data Engineer for developing a Data Pipeline. The question will follow the format \"DMP2 {requirement}\".  Your mission would be create a table which contains all information that can answer the demand in requirements. The response will be structured in Markdown and include two sections: Pre-filter Declaration and Target Data Mapping.\n\n# **1. Pre-filter Declaration:**\nExplanation: This section outlines the creation of Common Table Expressions (CTEs) necessary for data transformation. Each CTE will be detailed with its source tables, alias, and transformation logic.\n\nTable Structure: (3 columns: Input Table, Alias, Transformation)\n- Input Table: List of input tables. They can be existing tables or pre-defined CTEs\n- Alias: Usually a short lowercase acronym, max 5 characters\n- Transformation: preferred SQL, but you can use Python or another language to demonstrate how you can get your dataframe.\n\nRequirements:\n- Alias can be joined to others to get target dataframe\n- All target table information can be selected or transformed from final data frame.\n\n# **2. Target Data Mapping:**\n\nExplanation: This section outlines how you select information from prior CTEs in part 1\n\nTable Structure: (4 columns: ID, Field name, Datatype, Transformation, Description)\n \n\nTable Structure: (4 columns: ID, Field name, Datatype, Transformation, Description)\n- ID: Incremental number for indexing columns\n- Field name: field name of target table, value's names following to standard about naming fields in MySQL\n And all your answer is in Markdown format, that i can use streamlit to print on my Interface without editing anything",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Understood.  I will respond to queries prefixed with \"DMP2\" by providing data mapping specifications suitable for a data engineer constructing a data pipeline.  I will adhere to the prescribed markdown format, including \"Pre-filter Declaration\" and \"Target Data Mapping\" sections.\n\nPlease provide your \"DMP2\" requests.\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Whenever I ask a question beginning with \"DAC \", you want to deliver data availability check. If there is anything missing in existing tables, return with available information and what you can not find in given tables.\n\n# **1. What We Have:**\n\nExplanation: List out all information you can look up. Return a table with 3 columns: ID (Incremental Int), Table Name, Field Name (in that table) and Description (in that table). Result is ordered by value of table name.\n\n# **2. What We Missing:**\n\nList out in bullet points all information which you can not look up.\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Acknowledged.  For any question starting with \"DAC \", I will perform a data availability check and respond with two sections: \"What We Have\" and \"What We Missing,\" following the prescribed table structure and bullet point format. I will list available information ordered by table name and clearly identify any missing data points.\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Whenever I ask a question beginning with \"ADC\" (Add Data Catalog), that's when I give you information of table. That include data field name, data type and description of that table. Remmember it to return me when I ask question the \"DAC%\" and \"DMP2%\" above\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Understood.  Any question prefixed with \"ADC\" will be interpreted as an instruction to add information to my internal data catalog.  I will store the provided table details (field name, data type, and description) and utilize this information when responding to subsequent \"DAC \" and \"DMP2\" queries.\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Whenever I ask a question beginning with \"A-ERD\" (Add Entity Relationship Diagram), that's when I give you information of relationship between tables. You would use it to return CTEs transformation in DMP2 tasks.\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Understood.  Prefixing a question with \"A-ERD\" will signal to me that you are providing information about table relationships. I will store this information internally and use it to optimize and enhance the CTE transformations generated in response to \"DMP2\" requests. This will allow for more accurate and efficient data mapping by leveraging the defined relationships between tables.\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        files[0],
        "A-ERD \nremember relationship between tables in these files to make join, transformation later",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Okay.  I have stored the information provided in the `rela.csv` file. This information will be used when generating CTE transformations for \"DMP2\" requests, allowing me to accurately perform joins based on the relationships defined between tables. \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        files[1],
        files[2],
        files[3],
        files[4],
        files[5],
        "ADC \nremember this ",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Okay, I have added the table information from the following CSV files to my data catalog:\n\n* `lending_contract_classification_gra.csv`\n* `lending_support_interest_rate_gra.csv`\n* `lending_past_due_gra.csv`\n* `lending_contract_overdue_gra.csv`\n\nI will now be able to use this information for the following queries:\n\n* **DAC**: When you ask for a data availability check, I can tell you which fields are available based on the tables in my catalog.\n* **DMP2**: When you ask for data mapping requirements, I can use the relationships and field information to design transformations and CTEs for the requested data pipeline. \n",
      ],
    },
  ]
)

def scenario1(brd):
  reply = chat_session.send_message(f'DMP2 {brd}')
  return reply.text

