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
INTERVALLE = 60 * 60  # 1 heure en secondes

data_base = {
    "name": "CBN Arena",
    "clockTime": 3,
    "clockIncrement": 2,
    "minutes": 60,
    "conditions.teamMember.teamId": "chessbot-network-cbn",
    "conditions.bots": "true",
}

for i in range(NB_TOURNOIS):
    numero = i + 1

    # Attendre une heure avant chaque tournoi, sauf le premier
    if i > 0:
        prochain_lancement = debut + i * INTERVALLE
        attente = prochain_lancement - time.time()

        if attente > 0:
            print(
                f"Tournoi {numero} dans "
                f"{attente / 60:.0f} minutes."
            )
            time.sleep(attente)

    debut = time.time() if i == 0 else debut

    data = data_base.copy()
    data["name"] = f"CBN Arena #{numero:02d}"

    print(
        f"\n[{datetime.now().strftime('%H:%M:%S')}] "
        f"Création du tournoi {numero}/{NB_TOURNOIS}"
    )

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            data=data,
            timeout=30,
        )

        if response.ok:
            tournoi = response.json()
            print("✅ Tournoi créé :", data["name"])
            print(
                "Lien :",
                f"https://lichess.org/tournament/{tournoi['id']}"
            )
        else:
            print("❌ Erreur :", response.status_code)
            print(response.text)

    except requests.RequestException as e:
        print("❌ Erreur réseau :", e)

print("\n🏁 Planning des 12 tournois terminé.")
