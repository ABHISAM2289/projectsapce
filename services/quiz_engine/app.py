from flask import Flask, request, jsonify, send_from_directory
import json
import os
import requests
import re

app = Flask(__name__)

SUMMARY_FILE = "summary.json"
GEMINI_API_KEY = "AIzaSyAjcs77CwCgqvGxZ4b_8TbBmS7bSGWtMYo"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

def generate_quiz_from_summary():
    if not os.path.exists(SUMMARY_FILE):
        print("❌ Summary file not found.")
        return None

    with open(SUMMARY_FILE, "r") as f:
        summary_data = json.load(f)

    summary_text = summary_data.get("summary") or summary_data.get("transcript") or ""
    if not summary_text:
        print("❌ Summary text is empty.")
        return None

    prompt = f"""
    Based on the following summary, generate a JSON quiz with 5 questions.
    Each question should have 4 options labeled a–d and a correct answer as a single letter.
    Format output like this:

    {{
      "quiz": [
        {{
          "question": "What is ...?",
          "options": ["a) Option A", "b) Option B", "c) Option C", "d) Option D"],
          "answer": "a"
        }},
        ...
      ]
    }}

    Summary:
    {summary_text}
    """

    headers = {
        "Content-Type": "application/json"
    }

    body = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()

        content = data["candidates"][0]["content"]["parts"][0]["text"]

        # Extract and parse JSON
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if json_match:
            quiz_json = json.loads(json_match.group())
            return quiz_json.get("quiz", None)
        else:
            print("❌ Could not parse JSON from response.")
            return None

    except Exception as e:
        print("❌ Gemini API Error:", e)
        print("Response Text:", response.text if 'response' in locals() else 'No response')
        return None

@app.route("/")
def serve_frontend():
    return send_from_directory(".", "quiz.html")

@app.route("/quiz", methods=["GET"])
def get_quiz():
    quiz = generate_quiz_from_summary()
    if quiz is None:
        return jsonify({"error": "Quiz generation failed."}), 500

    quiz_no_answers = [{"question": q["question"], "options": q["options"]} for q in quiz]
    return jsonify({"quiz": quiz_no_answers})

@app.route("/submit", methods=["POST"])
def submit_answers():
    data = request.json
    user_answers = data.get("answers", [])
    quiz = generate_quiz_from_summary()

    if quiz is None:
        return jsonify({"error": "Quiz generation failed."}), 500

    if len(user_answers) != len(quiz):
        return jsonify({"error": "Answer count mismatch."}), 400

    score = 0
    feedback = []

    for i, user_ans in enumerate(user_answers):
        correct_answer = quiz[i]["answer"].lower()
        is_correct = user_ans.lower() == correct_answer
        if is_correct:
            score += 1
        feedback.append({
            "question": quiz[i]["question"],
            "your_answer": user_ans,
            "correct_answer": correct_answer,
            "correct": is_correct
        })

    return jsonify({
        "score": score,
        "total": len(quiz),
        "feedback": feedback
    })

if __name__ == "__main__":
    app.run(port=5003, debug=True)
