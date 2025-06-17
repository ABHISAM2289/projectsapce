import google.generativeai as genai

# Replace with your actual Gemini API key
genai.configure(api_key="AIzaSyAjcs77CwCgqvGxZ4b_8TbBmS7bSGWtMYo")

for model in genai.list_models():
    print(model.name)
