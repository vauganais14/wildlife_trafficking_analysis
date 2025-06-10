import pandas as pd
import os

# Chemin du fichier source
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.abspath(os.path.join(BASE_DIR, "../data/cites_clean_large.csv"))
OUTPUT_PATH = os.path.abspath(os.path.join(BASE_DIR, "../data/suspicious_trades.csv"))

# Paramètres de seuils
QUANTITY_THRESHOLD = 1000  # quantité jugée anormalement élevée

def detect_suspicious_trades():
    print("Chargement des données...")
    df = pd.read_csv(CSV_PATH)
    print(f"Nombre total de lignes chargées : {len(df)}")

    # Détection des cas suspects

    # Règle 1 : Exporter == Importer
    rule_same_country = df["Exporter"] == df["Importer"]

    # Règle 2 : Quantity anormalement élevée
    rule_high_quantity = df["Quantity"] > QUANTITY_THRESHOLD

    # Règle 3 : Purpose ou Source manquants
    rule_missing_info = df["Purpose"].isnull() | df["Source"].isnull()

    # Combinaison des règles
    suspicious_mask = rule_same_country | rule_high_quantity | rule_missing_info

    # Filtrage
    suspicious_df = df[suspicious_mask]

    # Sauvegarde
    print(f"Nombre de lignes suspectes détectées : {len(suspicious_df)}")
    suspicious_df.to_csv(OUTPUT_PATH, index=False)
    print(f"Fichier suspicious_trades.csv généré dans : {OUTPUT_PATH}")

if __name__ == "__main__":
    print("lancement du script")
    detect_suspicious_trades()
