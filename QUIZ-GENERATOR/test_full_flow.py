import requests

with open("example.txt", "rb") as f:
    response = requests.post("http://127.0.0.1:5004/generate-full-quiz", files={"file": f})
    print(response.json())
