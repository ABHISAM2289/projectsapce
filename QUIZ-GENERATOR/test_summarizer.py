import requests

url = "http://127.0.0.1:5002/summarize"

data = {
    "text": """The laws of thermodynamics, we start with the zeroth law to Define temperature. It talks about thermal equilibrium, where no heat is exchanged, no heat exchange than they must be the same temperature. And that's where that came from. Basically think, transitive property to assist amazed in thermal equilibrium with system. B and system, B is in thermal equilibrium with system C. Then a must be in thermal equilibrium with c. And all of them are the same temperature for the first sloth, in conservation of energy. It can't be created or destroyed. Can only change forms for this one. The change in  Internal energy of a system is equal to its heat transfer - the work. For example heat a cylinder mix the gas within expand and push the Piston up the heat entering - the energy devoted to the work equals, the total change in energy during the process for the second law and Chaos because the universe is constantly becoming more and more chaotic through entropy which explains why heat naturally flows from hot to cold and not cold to hot since things can't spontaneously become ordered and for the third law this one defines absolute zero basically. I absolutely  80, there's no change in entropy. So no increase in disorder, and for pure crystals, with no defects, it's entropy becomes zero."""
}

response = requests.post(url, json=data)

print("Response:", response.json())
