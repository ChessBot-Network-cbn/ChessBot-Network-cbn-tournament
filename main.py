
import os
import requests
import time

TOKEN = os.environ["LICHESS_TOKEN"]
API_URL = "https://lichess.org/api/tournament"

headers = {
    "Authorization": f"Bearer {TOKEN}",
}

# Paramètres communs aux 12 tournois
NB_TOURNOIS = 12

data_base = {
    "name": "CBN Arena",
    "clockTime": 3,
    "clockIncrement": 2,
    "minutes": 60,

    # Réserver aux membres de l'équipe CBN
    "conditions.teamMember.teamId": "chessbot-network-cbn",

    # Autoriser les bots, si Lichess accepte ce paramètre
    "conditions.bots": "true",
}

tournois_crees = []

for i in range(1, NB_TOURNOIS + 1):
    data = data_base.copy()

    # Un nom différent pour chaque tournoi
    data["name"] = f"CBN Arena"

    print(f"\nCréation du tournoi {i}/{NB_TOURNOIS}...")

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            data=data,
            timeout=30,
        )

        if response.ok:
            tournoi = response.json()
            tournoi_id = tournoi["id"]
            lien = f"https://lichess.org/tournament/{tournoi_id}"

            tournois_crees.append(lien)

            print(f"✅ {data['name']} créé !")
            print("Lien :", lien)
            print("Durée :", tournoi.get("minutes"), "minutes")
        else:
            print(f"❌ Échec du tournoi {i}")
            print("Erreur HTTP :", response.status_code)
            print(response.text)

    except requests.RequestException as e:
        print(f"❌ Erreur réseau pour le tournoi {i} :", e)

    # Petite pause entre les requêtes
    if i < NB_TOURNOIS:
        time.sleep(2)

print("\n========== RÉSULTAT ==========")
print(f"Tournois créés : {len(tournois_crees)}/{NB_TOURNOIS}")

for lien in tournois_crees:
    print(lien)
