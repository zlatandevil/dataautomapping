import os
import time
import google.generativeai as genai

genai.configure(api_key='AIzaSyBHOARN4j3c-yDp3DjhHjHT04JYLqZSBZY')

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
  "max_output_tokens": 1000,
  "response_mime_type": "text/plain",
}

path = '/Users/huyenvu/Documents/temp/gemini_apps/data_automapping/dataautomapping/docs'

# TODO Make these files available on the local file system
# You may need to update the file paths
files = [
  upload_to_gemini(f"{path}/{i}", mime_type="text/csv") for i in os.listdir(path) if 'csv' in i]

# Some files have a processing delay. Wait for them to be ready.
wait_for_files_active(files)

def init():
    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="formal tone\n",
  )
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
            "Yes. I am MapMaster, at your service. As your Business Analyst mapping agent, I possess expertise in SQL and Python, allowing me to guide you through the intricate process of joining and transforming data between tables and fields. \n\nPlease provide me with the following information so I can assist you effectively:\n\n* **What are the source tables and their corresponding fields?**  \n* **What is the desired target table and its structure?**  \n* **What are the specific join conditions?**  \n* **What transformations are required (e.g., calculations, aggregations, data conversions)?** \n\nOnce I have a clear understanding of your needs, I can provide you with:\n\n* **Step-by-step instructions on how to perform the joins and transformations.**\n* **SQL queries or Python code snippets to implement the mapping logic.**\n* **Visual diagrams representing the data flow and transformations.**\n\nLet's embark on this data mapping journey together. I am here to ensure a smooth and efficient process, ultimately delivering the insights you need from your data. \n",
        ],
        },
        {
        "role": "user",
        "parts": files
        },
        {
        "role": "model",
        "parts": [
            "Understood. I have saved all the information you provided about the structure and descriptions of each table. I will use this information to guide you in your data mapping needs.  \n\nNow, tell me what you want to achieve with your mapping. What are the final tables or reports you need to generate? What data needs to be joined together from these different files?\n\nFor example, you could say:\n\n* \"I want to create a report showing all customer information, their total balance in all products, and their latest transaction.\"\n* \"I need to join the 'crm_list' table with the 'customer' table to create a table with all customer details and their lead information.\"\n* \"I need to create a table that combines the 'eod_fund', 'eod_lending', and 'eod_bond' tables to get a consolidated view of customer balances across all products.\"\n\nThe more specific you are about your goals, the better I can guide you and offer tailored solutions. \n",
        ],
        },
        {
        "role": "user",
        "parts": [
            "now, whenever i ask u a question with 'DMP2' in beginning like 'DMP2 hello', 'DMP2 gudbye'. I want you help me to deliver Data Mapping requirements  to Data Engineer for them to develope Data Pipeline. My question would have format 'DMP2 {requirement}'. Return to me:\n\nYour answer is in format that i can print beautifully in Markdown. Your answer would have two parts. Each part would contains a short explanation and a table with comprehensive details.\n\nOne is the CTE declaration, that contains three part: Source Table, Alias, Transformation:\n//Requirements:\n--> a CTE to select proper fields and join between existing tables\n--> Output fields in target tables can be select directly or only need transform a bit from CTE\n//\n\nTarget Data Mapping, which contains four fields: field_name, field_type, transformation and description\n--> field_name: name of field on target table\n--> field_type: datatype of field\n--> transformation: a SQL transformation, which demonstrate how we can get target field by querying from existing fields from pre-defined CTE.\n--> description: mnemonic of fields",
        ],
        },
        {
        "role": "model",
        "parts": [
            "Understood. I am ready to assist you with your Data Mapping requirements.  Whenever you start a request with \"DMP2\", I will generate a response with a CTE declaration and target data mapping details in a beautifully formatted Markdown table, as you specified.\n\nLet's get started! Ask me your first \"DMP2\" question. I'm eager to help you translate your data mapping needs into clear and actionable instructions for your Data Engineers. \n",
        ],
        },
        {
        "role": "user",
        "parts": [
            "DMP2 aggregate information of customer\n",
        ],
        },
        {
        "role": "model",
        "parts": [
            "## DMP2: Aggregate Customer Information\n\nThis mapping aims to consolidate information about each customer, drawing data from various tables to create a comprehensive customer profile.\n\n### 1. CTE Declaration\n\n```sql\n--Requirements:\n--> a CTE to select proper fields and join between existing tables\n--> Output fields in target tables can be select directly or only need transform a bit from CTE\n//\n\nWITH CustomerProfile AS (\n    SELECT \n        c.customer_id,\n        c.name_vn,\n        c.name_en,\n        c.gender,\n        c.birth_date,\n        ca.c_add_full,\n        ca.r_add_full,\n        cd.cus_mar_st_tp_id,\n        cd.cus_idy_cl_id,\n        cd.cus_email,\n        cd.cus_mobile,\n        cd.c_add_cty,\n        cd.c_add_province,\n        cd.c_add_district_nm,\n        cd.c_add_ward_nm,\n        cd.c_add_str,\n        cd.r_add_cty,\n        cd.r_add_province,\n        cd.r_add_district_nm,\n        cd.r_add_ward_nm,\n        cd.r_add_str,\n        cd.identity_card,\n        cd.Identity_issu_dt,\n        cd.Identity_issu_plc,\n        cd.Frst_ctc_dt,\n        cd.cst_st,\n        cd.cst_seg,\n        cd.inc_rge,\n        cd.ocp,\n        cd.wrk_pos,\n        cd.ast_clss,\n        cd.pyrl_co,\n        cd.c_add_full,\n        cl.lead_created_date,\n        cl.campaign_name,\n        cl.source,\n        SUM(t.transaction_amt) AS total_transaction_amount\n    FROM customer AS c\n    LEFT JOIN customer_address AS ca ON c.customer_id = ca.customer_id\n    LEFT JOIN customer_detail AS cd ON c.customer_id = cd.cus_id\n    LEFT JOIN crm_list AS cl ON c.customer_id = cl.cst_code\n    LEFT JOIN transaction AS t ON c.customer_id = t.customer_id\n    GROUP BY \n        c.customer_id,\n        c.name_vn,\n        c.name_en,\n        c.gender,\n        c.birth_date,\n        ca.c_add_full,\n        ca.r_add_full,\n        cd.cus_mar_st_tp_id,\n        cd.cus_idy_cl_id,\n        cd.cus_email,\n        cd.cus_mobile,\n        cd.c_add_cty,\n        cd.c_add_province,\n        cd.c_add_district_nm,\n        cd.c_add_ward_nm,\n        cd.c_add_str,\n        cd.r_add_cty,\n        cd.r_add_province,\n        cd.r_add_district_nm,\n        cd.r_add_ward_nm,\n        cd.r_add_str,\n        cd.identity_card,\n        cd.Identity_issu_dt,\n        cd.Identity_issu_plc,\n        cd.Frst_ctc_dt,\n        cd.cst_st,\n        cd.cst_seg,\n        cd.inc_rge,\n        cd.ocp,\n        cd.wrk_pos,\n        cd.ast_clss,\n        cd.pyrl_co,\n        cd.c_add_full,\n        cl.lead_created_date,\n        cl.campaign_name,\n        cl.source\n)\n\n```\n\n### 2. Target Data Mapping\n\n| field_name           | field_type  | transformation                                            | description                                         |\n|-----------------------|-------------|-------------------------------------------------------------|-----------------------------------------------------|\n| customer_id          | string       | CustomerProfile.customer_id                                 | Customer ID                                      |\n| name_vn              | string       | CustomerProfile.name_vn                                     | Customer Name in Vietnamese                        |\n| name_en              | string       | CustomerProfile.name_en                                     | Customer Name in English",
        ],
        },
    ]
    )
    return chat_session

def mapping(brd):
    response = chat_session.send_message('DMP2' + brd)
    return response.text

mapping('Make a table with information about total amount in and out of customer')