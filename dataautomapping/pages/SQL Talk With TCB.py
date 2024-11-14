import google.generativeai as genai

def init_model():
    genai.configure(api_key="AIzaSyCn9L6fMD6ORt0b21mmVXBH0lQnFaYH7i8")
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model

print(type(init_model()))