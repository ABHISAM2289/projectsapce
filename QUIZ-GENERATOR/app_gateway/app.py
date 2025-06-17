from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/generate-full-quiz', methods=['POST'])
def full_flow():
    file = request.files['file']

    # 1. Upload the file
    upload_resp = requests.post("http://127.0.0.1:5001/upload", files={'file': file})
    filepath = upload_resp.json()['filepath']

    # 2. Summarize the content
    summarize_resp = requests.post("http://127.0.0.1:5003/summarize", json={"filepath": filepath})
    summary = summarize_resp.json()['summary']

    # 3. Generate quiz
    quiz_resp = requests.post("http://127.0.0.1:5002/generate-quiz", json={"summary": summary})
    quiz = quiz_resp.json()['questions']

    return jsonify({"quiz": quiz})

if __name__ == "__main__":
    app.run(port=5004)
