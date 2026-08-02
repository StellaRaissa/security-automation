fichier_blacklist = open("blacklist.txt", "r")
iocs_malveillants = fichier_blacklist.read().splitlines()
fichier_blacklist.close()

fichier_a_verifier = open("a_verifier.txt", "r")
adresses_a_verifier = fichier_a_verifier.read().splitlines()
fichier_a_verifier.close()

nombre_menaces = 0

print("=== Rapport de verification IOC ===")

for adresse in adresses_a_verifier:
    if adresse in iocs_malveillants:
        print("[ALERTE] " + adresse + " est malveillante !")
        nombre_menaces = nombre_menaces + 1
    else:
        print("[OK] " + adresse + " est inconnue.")

print("===================================")
print("Adresses verifiees : " + str(len(adresses_a_verifier)))
print("Menaces detectees : " + str(nombre_menaces))
