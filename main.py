
import os
import requests
import time
from datetime import datetime

TOKEN = os.environ["LICHESS_TOKEN"]
API_URL = "https://lichess.org/api/tournament"

headers = {
    "Authorization": f"Bearer {TOKEN}",
}

NB_TOURNOIS = 12
INTERVALLE = 60 * 60 * 1000  # 1 heure en millisecondes

# Premier tournoi programmé dans 2 minutes
# pour laisser le temps aux joueurs de rejoindre.
premier_depart = int(time.time() * 1000) + 2 * 60 * 1000

data_base = {
    "name": "CBN",
    "clockTime": 3,
    "clockIncrement": 2,
    "minutes": 60,
    "conditions.teamMember.teamId": "chessbot-network-cbn",
    "conditions.bots": "true",
}

tournois_crees = []

print("🚀 Lancement de la création des 12 tournois CBN Arena\n")

for i in range(NB_TOURNOIS):

    numero = i + 1

    # Calcul du démarrage prévu
    date_depart = premier_depart + i * INTERVALLE

    data = data_base.copy()
    data["startDate"] = date_depart

    heure_depart = datetime.fromtimestamp(
        date_depart / 1000
    ).strftime("%d/%m/%Y à %H:%M:%S")

    print(f"[{datetime.now().strftime('%H:%M:%S')}] "
          f"Création du tournoi {numero}/{NB_TOURNOIS}")

    print(f"🕒 Départ prévu : {heure_depart}")

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            data=data,
            timeout=30,
        )

        if response.ok:
            tournoi = response.json()

            lien = f"https://lichess.org/tournament/{tournoi['id']}"

            tournois_crees.append(lien)

            print("✅ Tournoi créé !")
            print("🔗", lien)

        else:
            print("❌ Erreur HTTP :", response.status_code)
            print(response.text)

    except requests.RequestException as e:
        print("❌ Erreur réseau :", e)

    print("-" * 50)

print("\n🏁 CRÉATION TERMINÉE")
print(f"Tournois créés : {len(tournois_crees)}/{NB_TOURNOIS}")

print("\n📋 LIENS DES TOURNOIS :")

for lien in tournois_crees:
    print(lien)
