import requests

url = "http://127.0.0.1:5003/generate_quiz"

data = {
    "text": """The laws of thermodynamics describe energy behavior. The Zeroth Law defines temperature through thermal equilibrium. The First Law states energy is conserved. The Second Law introduces entropy and the tendency toward disorder. The Third Law relates to absolute zero."""
}

response = requests.post(url, json=data)
print("Quiz:\n", response.json())
