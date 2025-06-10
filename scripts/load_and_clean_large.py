import pandas as pd
import glob
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.abspath(os.path.join(BASE_DIR, "../data/"))
OUTPUT_FILE = os.path.abspath(os.path.join(BASE_DIR, "../data/cites_clean_large.csv"))

# Colonnes à conserver
COLUMNS_TO_KEEP = [
    "Year", "Taxon", "Quantity", "Unit", "Importer", "Exporter", "Origin", "Purpose", "Source"
]

# Filtres à appliquer
MIN_YEAR = 2000

def process_one_file(file_path):
    try:
        print(f"Traitement de : {file_path}")
        df = pd.read_csv(file_path, low_memory=False)

        # Filtrage colonnes
        df = df[COLUMNS_TO_KEEP]

        # Conversion année
        df["Year"] = pd.to_numeric(df["Year"], errors='coerce')
        df = df[df["Year"] >= MIN_YEAR]

        # Quantité → numérique
        df["Quantity"] = pd.to_numeric(df["Quantity"], errors='coerce')
        df = df.dropna(subset=["Quantity"])

        return df

    except Exception as e:
        print(f"Erreur sur {file_path} : {e}")
        return pd.DataFrame()  # dataframe vide si erreur

def process_all_files(folder_path):
    print("DEBUT process_all_files") 
    all_files = glob.glob(os.path.join(folder_path, "*.csv"))
    print(f"{len(all_files)} fichiers détectés.")
    print(f"DEBUG: fichiers trouvés = {all_files}")


    full_df = pd.DataFrame()
    for file in all_files:
        df_part = process_one_file(file)
        full_df = pd.concat([full_df, df_part], ignore_index=True)

    print(f"Nombre total de lignes après nettoyage : {len(full_df)}")
    full_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Fichier final sauvegardé dans : {OUTPUT_FILE}")

if __name__ == "__main__":
    process_all_files(DATA_FOLDER)