import json

fichier = open("eve.json", "r")
lignes = fichier.read().splitlines()
fichier.close()

nombre_alertes = 0
rapport = ""

rapport = rapport + "==Analyse des logs suricata ==\n"

for ligne in lignes:
    evenement = json.loads(ligne)
    if evenement["event_type"] == "alert":
        nombre_alertes = nombre_alertes + 1
        ip_source = evenement["src_ip"]
        signature = evenement["alert"]["signature"]
        rapport = rapport + "[ALERTE] " + ip_source + " -> " + signature + "\n"

rapport = rapport + "===============================================\n"
rapport = rapport + "Alertes trouvees : " + str(nombre_alertes) + "\n"

print(rapport)

fichier_rapport = open("rapport.txt", "w")
fichier_rapport.write(rapport)
fichier_rapport.close()

print("== Rapport sauvegarde dans rapport.txt ==")
