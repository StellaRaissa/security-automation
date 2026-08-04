import requests
import time
from config import API_KEY

fichier = open("a_verifier.txt", "r")
adresses = fichier.read().splitlines()
fichier.close()

headers = {"x-apikey": API_KEY}

print("== Scan VirusTotal ==")

for ip in adresses:
    url = "https://www.virustotal.com/api/v3/ip_addresses/" + ip
    reponse = requests.get(url, headers=headers)
    donnees = reponse.json()

    statistiques = donnees["data"]["attributes"]["last_analysis_stats"]
    malveillant = statistiques["malicious"]

    if malveillant > 0:
        print("[ALERTE] " + ip + " → " + str(malveillant) + " moteurs la signalent")
    else:
        print("[OK] " + ip + " → propre")

    time.sleep(15)

print("== Scan termine ==")
