import google.generativeai as genai
import google.generativeai as genai

# Set your API key
api_key = "YOUR_API_KEY"
genai.configure(api_key="AIzaSyCn9L6fMD6ORt0b21mmVXBH0lQnFaYH7i8")

# Specify the model
model = genai.GenerativeModel("gemini-1.5-pro")

# Send a message and get the response
prompt = "Write a Python function to reverse a string."
response = model.generate_content(prompt=prompt, model=model)

# Extract the text response
text_response = response.text

# Print the response in Markdown format
print(text_response)

