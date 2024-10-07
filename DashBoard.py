import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("players_data.csv")

df = df.rename(columns={
    'Pos': 'Position',
    'Nation': 'Nationality',
    'Ast': 'Assists',
    'Min': 'Minutes',
    'Comp': 'League'
})

if 'Minutes' in df.columns:
    df['Matches'] = df['Minutes'] / 90  

if 'Gls' in df.columns and 'Matches' in df.columns:
    df['Buts/Match'] = df['Gls'] / df['Matches']
if 'Assists' in df.columns and 'Matches' in df.columns:
    df['Assists/Match'] = df['Assists'] / df['Matches']

if 'Gls' in df.columns and 'Assists' in df.columns:
    df['Contributions Totales'] = df['Gls'] + df['Assists']

st.title("Dashboard d'Analyse des Joueurs de Football")

st.subheader("Classement des Meilleurs Buteurs par Nombre de Buts")
if 'Gls' in df.columns:
    top_scorers = df[['Player', 'Nationality', 'Position', 'League', 'Gls']].sort_values(by='Gls', ascending=False).head(10)
    st.table(top_scorers.style.format({'Gls': '{:.0f}'}).background_gradient(cmap='YlGnBu'))

st.subheader("Classement des Meilleurs Passeurs par Nombre de Passes Décisives")
if 'Assists' in df.columns:
    top_assisters = df[['Player', 'Nationality', 'Position', 'League', 'Assists']].sort_values(by='Assists', ascending=False).head(10)
    st.table(top_assisters.style.format({'Assists': '{:.0f}'}).background_gradient(cmap='Oranges'))

st.subheader("Classement des Meilleurs Contributeurs (Buts + Assists)")
if 'Contributions Totales' in df.columns:
    top_contributors = df[['Player', 'Nationality', 'Position', 'League', 'Gls', 'Assists', 'Contributions Totales']].sort_values(by='Contributions Totales', ascending=False).head(10)
    st.table(top_contributors.style.format({'Contributions Totales': '{:.0f}', 'Gls': '{:.0f}', 'Assists': '{:.0f}'}).background_gradient(cmap='RdYlGn'))

st.subheader("Performances Moyennes par Position")
if 'Position' in df.columns and 'Buts/Match' in df.columns and 'Assists/Match' in df.columns:
    avg_stats_by_position = df.groupby('Position').agg({
        'Buts/Match': 'mean',
        'Assists/Match': 'mean',
        'Minutes': 'mean'
    }).reset_index()
    fig, ax = plt.subplots(figsize=(14, 7))
    avg_stats_by_position.set_index('Position')[['Buts/Match', 'Assists/Match', 'Minutes']].plot(kind='bar', ax=ax, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    plt.title("Performances Moyennes par Position (Buts/Match, Assists/Match, Minutes)", fontsize=16)
    plt.xlabel("Position", fontsize=14)
    plt.ylabel("Moyennes", fontsize=14)
    plt.xticks(rotation=45)
    for container in ax.containers:
        ax.bar_label(container, label_type='center')
    plt.grid(axis='y')
    st.pyplot(fig)

st.subheader("Comparaison des Performances Moyennes par Ligue")
if 'League' in df.columns:
    league_comparison = df.groupby('League').agg({
        'Buts/Match': 'mean',
        'Assists/Match': 'mean',
        'Minutes': 'mean'
    }).reset_index()
    fig, ax = plt.subplots(figsize=(14, 7))
    league_comparison.set_index('League')[['Buts/Match', 'Assists/Match', 'Minutes']].plot(kind='bar', ax=ax, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    plt.title("Performances Moyennes par Ligue (Buts/Match, Assists/Match, Minutes)", fontsize=16)
    plt.xlabel("Ligue", fontsize=14)
    plt.ylabel("Moyennes", fontsize=14)
    plt.xticks(rotation=45)
    for container in ax.containers:
        ax.bar_label(container, label_type='center')
    plt.grid(axis='y')
    st.pyplot(fig)

if 'League' in df.columns:
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x='League', y='Gls', data=df, palette='coolwarm', ax=ax)
    plt.title("Distribution des buts par ligue", fontsize=16)
    plt.xlabel("Ligue", fontsize=14)
    plt.ylabel("Nombre de buts", fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    st.pyplot(fig)
