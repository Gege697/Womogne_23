# Importation des modules
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------
# Fichier de stockage
# -----------------------------
DATA_FILE = "resultats.xlsx"

# Création du fichier si absent
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=[
        "Nom du projet", "Localisation", "Type de travaux",
        "Durée (mois)", "Qualité matériaux", "Respect délais",
        "Sécurité", "Propreté", "Commentaires"
    ])
    df_init.to_excel(DATA_FILE, index=False)

# -----------------------------
# Titre de l'application
# -----------------------------
st.title("📊 Sondage Génie Civil")
st.write("Merci de remplir ce formulaire pour nous aider à améliorer nos projets.")

# -----------------------------
# Formulaire
# -----------------------------
with st.form("form_sondage"):
    st.subheader("Informations sur le projet")
    projet = st.text_input("Nom du projet")
    localisation = st.text_input("Localisation / site")
    type_travaux = st.selectbox("Type de travaux", ["Construction", "Réhabilitation", "Ponts et routes", "Bâtiment industriel"])
    duree = st.number_input("Durée des travaux (mois)", min_value=1, max_value=120, step=1)

    st.subheader("Évaluation")
    qualite = st.selectbox("Qualité des matériaux", ["Très satisfaisant", "Satisfaisant", "Moyen", "Insatisfaisant"])
    delais = st.selectbox("Respect des délais", ["Oui", "Partiellement", "Non"])
    securite = st.selectbox("Sécurité sur le chantier", ["Très bonne", "Bonne", "Moyenne", "Mauvaise"])
    proprete = st.selectbox("Propreté du chantier", ["Très bonne", "Bonne", "Moyenne", "Mauvaise"])

    commentaires = st.text_area("Commentaires / Suggestions")

    submit = st.form_submit_button("Envoyer")

# -----------------------------
# Gestion de l'envoi
# -----------------------------
if submit:
    if not projet or not localisation:
        st.error("Veuillez remplir tous les champs obligatoires.")
    else:
        # Chargement et ajout des données
        try:
            df = pd.read_excel(DATA_FILE)
        except:
            df = pd.DataFrame(columns=[
                "Nom du projet", "Localisation", "Type de travaux",
                "Durée (mois)", "Qualité matériaux", "Respect délais",
                "Sécurité", "Propreté", "Commentaires"
            ])
        new_row = pd.DataFrame({
            "Nom du projet": [projet],
            "Localisation": [localisation],
            "Type de travaux": [type_travaux],
            "Durée (mois)": [duree],
            "Qualité matériaux": [qualite],
            "Respect délais": [delais],
            "Sécurité": [securite],
            "Propreté": [proprete],
            "Commentaires": [commentaires]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_excel(DATA_FILE, index=False)
        st.success("✅ Réponse enregistrée ! Merci pour votre participation.")

# -----------------------------
# Diagramme en barres
# -----------------------------
st.subheader("📈 Répartition des avis sur la qualité des matériaux")

try:
    df_plot = pd.read_excel(DATA_FILE)
except:
    df_plot = pd.DataFrame()

if df_plot.empty or "Qualité matériaux" not in df_plot.columns:
    st.info("Aucune donnée pour le moment.")
else:
    counts = df_plot["Qualité matériaux"].value_counts()

    fig, ax = plt.subplots()
    ax.bar(counts.index, counts.values)

    ax.set_xlabel("Niveau de qualité")
    ax.set_ylabel("Nombre de réponses")
    ax.set_title("Avis sur la qualité des matériaux")

    plt.xticks(rotation=15)

    st.pyplot(fig)