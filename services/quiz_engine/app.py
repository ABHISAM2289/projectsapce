from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Set your Gemini API key
genai.configure(api_key="AIzaSyAjcs77CwCgqvGxZ4b_8TbBmS7bSGWtMYo")

# Load the Gemini model
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

@app.route("/", methods=["GET"])
def home():
    return "Auto Quiz Generator is running!"

@app.route("/generate-quiz", methods=["POST"])
def generate_quiz():
    try:
        data = request.get_json()
        summary = data.get("summary")

        if not summary:
            return jsonify({"error": "Summary is required"}), 400

        # Prompt for Gemini
        prompt = f"""
        Based on the following summary, generate 5 multiple-choice questions with 4 options each and indicate the correct answer.

        Summary:
        {summary}

        Format:
        [
          {{
            "question": "...",
            "options": ["A", "B", "C", "D"],
            "answer": "A"
          }},
          ...
        ]
        """

        response = model.generate_content(prompt)

        # Gemini usually returns a markdown or string, so parse it
        try:
            import json
            content = response.text
            start = content.find('[')
            end = content.rfind(']') + 1
            questions_json = json.loads(content[start:end])
        except Exception as e:
            return jsonify({"error": "Failed to parse Gemini response", "raw": content}), 500

        return jsonify({"questions": questions_json})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5002, debug=True)
