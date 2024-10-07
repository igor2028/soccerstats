import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Charger le dataset depuis un fichier CSV
df = pd.read_csv("players_data.csv")

# Vérifier les colonnes disponibles
print("Colonnes disponibles dans le DataFrame :", df.columns)

# Vérification des valeurs dupliquées
print("Valeurs dupliquées :", df.duplicated().sum())

# Suppression des doublons si nécessaire
df = df.drop_duplicates()

# Vérification des valeurs manquantes
print("Valeurs manquantes :\n", df.isnull().sum())

# Remplir les valeurs manquantes ou supprimer selon le cas
df['Gls'].fillna(0, inplace=True)

# Vérification des valeurs aberrantes
print("Valeurs aberrantes (Gls négatifs) :", (df['Gls'] < 0).sum())

# Suppression des valeurs aberrantes
df = df[df['Gls'] >= 0]

# Afficher les premières lignes du DataFrame
print(df.head())

# Afficher les statistiques descriptives
print(df.describe())

# Vérifier et ajuster les noms de colonnes si nécessaire
df = df.rename(columns={
    'position': 'Position',
    'nationality': 'Nationality',
    'minutes_played': 'MP',
    'goals': 'Gls',
    'league': 'League',
    'assists': 'Assists'
})

# Visualisation du nombre de joueurs par position
if 'Position' in df.columns:
    players_by_position = df['Position'].value_counts()
    players_by_position.plot(kind='bar', color='skyblue')
    plt.title("Nombre de joueurs par position")
    plt.xlabel("Position")
    plt.ylabel("Nombre de joueurs")
    plt.show()
else:
    print("La colonne 'Position' n'existe pas dans le DataFrame.")

# Visualisation du nombre de joueurs par nation
if 'Nationality' in df.columns:
    players_by_nation = df['Nationality'].value_counts().head(10)  # Afficher les 10 premières nations
    players_by_nation.plot(kind='bar', color='lightgreen')
    plt.title("Nombre de joueurs par nation (Top 10)")
    plt.xlabel("Nation")
    plt.ylabel("Nombre de joueurs")
    plt.show()
else:
    print("La colonne 'Nationality' n'existe pas dans le DataFrame.")

# Titre de l'application Streamlit
st.title("Dashboard d'Analyse des Joueurs de Football")

# Sélection des filtres pour la visualisation
if 'Position' in df.columns:
    position = st.sidebar.selectbox("Sélectionnez la position des joueurs", df['Position'].unique())
else:
    position = None

if 'MP' in df.columns:
    experience = st.sidebar.slider("Filtrer par minutes jouées (MP)", int(df['MP'].min()), int(df['MP'].max()))
else:
    experience = 0

if 'Gls' in df.columns:
    goals = st.sidebar.slider("Filtrer par nombre de buts (Gls)", int(df['Gls'].min()), int(df['Gls'].max()))
else:
    goals = 0

# Filtrage du dataframe selon les sélections de l'utilisateur
if position and 'MP' in df.columns and 'Gls' in df.columns:
    filtered_df = df[(df['Position'] == position) & (df['MP'] >= experience) & (df['Gls'] >= goals)]
    st.dataframe(filtered_df)
    st.bar_chart(filtered_df['Gls'])

# Visualisation de la distribution des buts par ligue
if 'League' in df.columns:
    sns.boxplot(x='League', y='Gls', data=df)
    plt.title("Distribution des buts par ligue")
    plt.xlabel("Ligue")
    plt.ylabel("Nombre de buts")
    plt.show()
else:
    print("La colonne 'League' n'existe pas dans le DataFrame.")

# Visualisation de la distribution des assists par ligue
if 'League' in df.columns and 'Assists' in df.columns:
    sns.boxplot(x='League', y='Assists', data=df)
    plt.title("Distribution des assists par ligue")
    plt.xlabel("Ligue")
    plt.ylabel("Nombre d'assists")
    plt.show()
else:
    print("Les colonnes 'League' ou 'Assists' n'existent pas dans le DataFrame.")

# Visualisation de la distribution des minutes jouées par ligue
if 'League' in df.columns and 'MP' in df.columns:
    sns.boxplot(x='League', y='MP', data=df)
    plt.title("Distribution des minutes jouées par ligue")
    plt.xlabel("Ligue")
    plt.ylabel("Minutes jouées")
    plt.show()
else:
    print("Les colonnes 'League' ou 'MP' n'existent pas dans le DataFrame.")

