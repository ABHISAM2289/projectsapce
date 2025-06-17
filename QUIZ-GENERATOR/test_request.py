import requests

url = "http://127.0.0.1:5002/generate-quiz"
payload = {
    "summary": "The heart is a muscular organ that pumps blood through the circulatory system. It supplies oxygen and nutrients and removes waste."
}

response = requests.post(url, json=payload)
print(response.json())
