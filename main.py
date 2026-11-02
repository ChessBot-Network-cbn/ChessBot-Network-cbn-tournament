
import os
import requests

TOKEN = os.environ["LICHESS_TOKEN"]
API_URL = "https://lichess.org/api/tournament"

headers = {
    "Authorization": f"Bearer {TOKEN}",
}

data = {
    "name": "CBN Arena",
    "clockTime": 3,
    "clockIncrement": 2,
    "minutes": 60,

    # Réserver le tournoi aux membres de l'équipe CBN
    "conditions.teamMember.teamId": "chessbot-network-cbn",

    # Demander à Lichess d'autoriser les bots
    "conditions.bots": "true",
}

response = requests.post(
    API_URL,
    headers=headers,
    data=data,
    timeout=30,
)

if response.ok:
    tournoi = response.json()
    print("CBN Arena créé !")
    print("Lien :", f"https://lichess.org/tournament/{tournoi['id']}")
    print("Durée :", tournoi.get("minutes"), "minutes")
    print("Bots autorisés :", tournoi.get("botsAllowed"))
else:
    print("Erreur :", response.status_code)
    print(response.text)
    raise SystemExit(1)

