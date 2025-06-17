from flask import Flask, request, jsonify
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)

# Configure Gemini API key
genai.configure(api_key="AIzaSyAjcs77CwCgqvGxZ4b_8TbBmS7bSGWtMYo")  # Replace with your actual API key

# Route for summarizing text
@app.route("/summarize", methods=["POST"])
def summarize_text():
    try:
        content = request.json["text"]

        # Initialize Gemini model
        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

        # Generate summary
        response = model.generate_content([f"Summarize the following content:\n{content}"])
        return jsonify({"summary": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Start the server
if __name__ == "__main__":
    app.run(port=5002, debug=True)
