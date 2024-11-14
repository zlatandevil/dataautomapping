import google.generativeai as genai
genai.configure(api_key='AIzaSyBHOARN4j3c-yDp3DjhHjHT04JYLqZSBZY')
def sumup(brd):
    model = genai.GenerativeModel("gemini-1.5-flash")
    reply = model.generate_content(f"""
        Sum up information in this Business Requirement Declaration 
        //"{brd}"//
        And list down all features this BRD look need to identify!
        Beautify your return in markdown as much as possible. At least beautify your list of features!
        Shorten your answer in 300 words!
        """)
    return reply.text

