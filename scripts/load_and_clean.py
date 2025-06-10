import pandas as pd
import glob
import os

# chemin vers tes csv CITES
DATA_FOLDER = "../data/"  # adapte si besoin si ton dossier est au même niveau

def load_all_csv(folder_path, limit_files=None):
    # cherche tous les CSV dans le dossier
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    print(f"{len(csv_files)} fichiers trouvés.")

    # Si limit_files est défini → on prend que les premiers
    if limit_files is not None:
        csv_files = csv_files[:limit_files]
        print(f"Limité à {len(csv_files)} fichiers.")

    # charge tous les CSV et concatène en un seul dataframe
    df_list = []
    for file in csv_files:
        print(f"Chargement : {file}")
        df = pd.read_csv(file, low_memory=False)  # low_memory=False pour éviter les warnings chiants
        df_list.append(df)

    # concatène tout
    full_df = pd.concat(df_list, ignore_index=True)
    return full_df


def clean_dataframe(df):
    # selectionne les colonnes utiles
    columns_to_keep = [
        'Year',
        'Taxon',
        'Quantity',
        'Unit',
        'Importer',
        'Exporter',
        'Origin',
        'Purpose',
        'Source'
    ]

    df = df[columns_to_keep]

    # Nettoyage de Quantity : convertir en numérique
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
    df = df.dropna(subset=['Quantity'])  # on supprime les lignes sans quantité

    return df

if __name__ == "__main__":
    df_raw = load_all_csv(DATA_FOLDER, limit_files=5)  # par exemple → charge juste 5 fichiers
    print(f"Nombre total de lignes chargées : {len(df_raw)}")

    df_clean = clean_dataframe(df_raw)
    print(f"Nombre de lignes après nettoyage : {len(df_clean)}")

    print("Aperçu des données :")
    print(df_clean.head())

    # Sauvegarde éventuelle du dataframe nettoyé pour aller plus vite ensuite
    df_clean.to_csv("../data/cites_clean.csv", index=False)
    print("Fichier nettoyé sauvé : data/cites_clean.csv")
