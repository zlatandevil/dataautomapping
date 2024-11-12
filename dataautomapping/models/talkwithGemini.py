import google.generativeai as genai
key = 'AIzaSyBHOARN4j3c-yDp3DjhHjHT04JYLqZSBZY'
def init():
    genai.configure(api_key=key)


    model = genai.GenerativeModel(
        "gemini-1.5-pro"
    )

    return model 

def chatbot(prompt):
    m = init()
    response = m.generate_content(prompt)
    return response.text

