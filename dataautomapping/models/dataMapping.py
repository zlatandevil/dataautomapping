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
path = "/Users/huyenvu/Documents/temp/gemini_apps/data_automapping/dataautomapping"
# TODO Make these files available on the local file system
# You may need to update the file paths
files = [
  upload_to_gemini(f"{path}/docs/idv_des.csv", mime_type="text/csv"),
  upload_to_gemini(f"{path}/docs/idv.csv", mime_type="text/csv"),
  upload_to_gemini(f"{path}/docs/org_des.csv", mime_type="text/csv"),
]

# Some files have a processing delay. Wait for them to be ready.
wait_for_files_active(files)

def scenario1(files):
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
          "Whenever I ask a question beginning with \"DMP2\", you want to deliver Data Mapping requirements to a Data Engineer for developing a Data Pipeline. The question will follow the format \"DMP2 {requirement}\".  Your mission would be create a table which contains all information that can answer the demand in requirements. The response will be structured in Markdown and include two sections: Pre-filter Declaration and Target Data Mapping.\n\n# **1. Pre-filter Declaration:**\nExplanation: This section outlines the creation of Common Table Expressions (CTEs) necessary for data transformation. Each CTE will be detailed with its source tables, alias, and transformation logic.\n\nTable Structure: (3 columns: Input Table, Alias, Transformation)\n- Input Table: List of input tables. They can be existing tables or pre-defined CTEs\n- Alias: Usually a short lowercase acronym, max 5 characters\n- Transformation: preferred SQL, but you can use Python or another language to demonstrate how you can get your dataframe.\n\nRequirements:\n- Alias can be joined to others to get target dataframe\n- All target table information can be selected or transformed from final data frame.\n\n# **2. Target Data Mapping:**\n\nExplanation: This section outlines how you select information from prior CTEs in part 1\n\nTable Structure: (4 columns: ID, Field name, Datatype, Transformation, Description)\n",
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
          files[1],
          files[2],
          "DMP2 information of organization representative\n",
        ],
      },
      {
        "role": "model",
        "parts": [
          "```markdown\n# DMP2 information of organization representative\n\n## 1. Pre-filter Declaration:\n\n| Input Table                                   | Alias | Transformation                                                                                                                                                                                                                                        |\n|-----------------------------------------------|-------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|\n| `tcb-prod-curated.organization_gra`           | org   | SELECT * FROM `tcb-prod-curated.organization_gra`                                                                                                                                                                                                   |\n| `tcb-prod-curated.individual_gra_ds1`        | idv   | SELECT * FROM `tcb-prod-curated.individual_gra_ds1`                                                                                                                                                                                                  |\n\n\n## 2. Target Data Mapping:\n\n| ID | Field name          | Datatype | Transformation                                                | Description                                                            |\n|----|----------------------|----------|------------------------------------------------------------|------------------------------------------------------------------------|\n| 1  | org_id              | STRING   | org.org_id                                                  | The unique identifier assigned to an Organization.                   |\n| 2  | representative_id   | STRING   | idv.individual_id                                          | The unique identifier assigned to an Individual representative.      |\n| 3  | representative_name | STRING   | idv.idv_name_vie                                            | Vietnamese name of the representative.                             |\n| 4  | representative_type | STRING   |  (requires further clarification on source and logic)       | Type of representative (e.g., legal representative, authorized signatory). It's currently unclear where this information resides.  |\n| ... | ...                   | ...      | ...                                                        | ...                                                                    |\n\n```\n\n**Explanation and Caveats:**\n\n* **Missing Information:**  The provided CSV files do not specify how `organization_gra` and `individual_gra_ds1` are linked.  Specifically, it is unclear how to identify which individuals are representatives of which organizations. The transformation for `representative_type` also requires more information.  To complete this mapping, details on the relationship between organizations and their representatives are required.  Examples of linking fields could include a dedicated representative ID within the organization table or a separate joining table.\n* **Assumptions:**  The above mapping assumes that `individual_id` in `individual_gra_ds1` can be used as `representative_id`.  This assumption may not be accurate without further clarification.  The `representative_type` field has been included as a placeholder, highlighting the missing information.\n* **Next Steps:**  To proceed, please provide the following:\n    * How are organizations and their representatives linked in the data?  Are there any specific fields that connect these two entities?\n    * Where is the information for `representative_type` stored? What are the possible values for this field?\n    * Please provide the schema or data dictionary for the involved tables if available.  This will help to identify relevant fields and ensure accurate mapping.\n\n\n\nOnce the missing information is provided, the mapping can be completed.\n",
        ],
      },
    ]
  )
  return chat_session