"""
Mon Assistante de Grossesse — Version finale by Maddy
-----------------------------------------------------

Améliorations :
✅ Nouveaux symptômes (maux de tête, reflux, sommeil, humeur)
✅ Design couleur personnalisée (#B32B69)
✅ Explications claires pour chaque symptôme
✅ Filtrage par mois
✅ Page de conseils
✅ Interface claire, bienveillante et fonctionnelle
"""

import streamlit as st
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt

# --- Configuration de la page ---
st.set_page_config(page_title="Mon Assistante de Grossesse", page_icon="🤰", layout="centered")

# --- Navigation ---
page = st.sidebar.selectbox("📋 Navigation", ["Suivi quotidien", "Conseils grossesse"], key="nav_page")

# --- Données ---
FICHIER = "symptomes.csv"

try:
    df = pd.read_csv(FICHIER)
except FileNotFoundError:
    df = pd.DataFrame(columns=[
        "Date", "Moment", "Fatigue", "Douleurs", "Nausees",
        "Maux_de_tete", "RGO", "Sommeil", "Humeur",
        "Contractions", "Remarques"
    ])

#  PAGE 1 : SUIVI QUOTIDIEN

if page == "Suivi quotidien":
    st.markdown("<h1 style='color:#B32B69;'>🤰 Mon Assistante de Grossesse</h1>", unsafe_allow_html=True)
    st.markdown("""
    Bienvenue dans votre espace de suivi de grossesse 💕  
    Notez vos symptômes chaque jour pour suivre leur évolution et recevoir un conseil adapté.  
    <br><br>
    <small style='color:gray;'>⚠️ Cette application est à visée éducative et ne remplace pas un avis médical.</small>
    """, unsafe_allow_html=True)

    # --- Saisie utilisateur ---
    st.markdown("<h2 style='color:#B32B69;'>🩺 Enregistrer une observation</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        moment = st.selectbox("Moment de la journée", ["Matin", "Soir"], key="moment_select")
        date_jour = st.date_input("Date du jour", date.today(), key="date_input")

    with col2:
        fatigue = st.slider("💤 Niveau de fatigue", 0, 10, 5, key="fatigue_slider")
        douleur = st.slider("💢 Douleurs corporelles (dos, bassin, jambes…)", 0, 10, 3, key="douleur_slider")

    # --- Bloc explicatif global ---
    st.progress(0)
    st.caption("🔹 0 = aucun symptôme  |  🔸 5 = modéré  |  🔺 10 = très intense")

    # --- Symptômes détaillés ---
    st.markdown("### 🌡️ Évaluation des symptômes du jour")

    nausees = st.slider("🤢 Nausées ou inconfort digestif", 0, 10, 2, key="nausees_slider")
    st.caption("0 = aucune nausée | 10 = nausées constantes ou fortes")

    maux_tete = st.slider("🤕 Maux de tête / migraines", 0, 10, 2, key="maux_tete_slider")
    st.caption("0 = aucun mal de tête | 10 = migraine intense")

    rgo = st.slider("🔥 Reflux ou brûlures d’estomac (RGO)", 0, 10, 2, key="rgo_slider")
    st.caption("0 = aucun reflux | 10 = brûlures très gênantes")

    with st.expander("😴 Qualité du sommeil — cliquez pour voir l’échelle détaillée"):
        st.markdown("""
        - **0** = Nuit très mauvaise (réveils fréquents, fatigue au réveil)  
        - **5** = Nuit moyenne (sommeil léger ou interrompu)  
        - **10** = Nuit excellente (repos complet, réveil en forme)
        """)
    sommeil = st.slider("Note du sommeil", 0, 10, 6, key="sommeil_slider")

    with st.expander("💖 Humeur / moral du jour — cliquez pour voir l’échelle détaillée"):
        st.markdown("""
        - **0** = Très bas moral, anxiété ou irritabilité marquée  
        - **5** = Moral neutre, journée correcte  
        - **10** = Très bon moral, pleine d’énergie et optimiste ✨
        """)
    humeur = st.slider("Note du moral", 0, 10, 7, key="humeur_slider")

    contractions = st.selectbox("Contractions ressenties ?", ["Non", "Légères", "Régulières"], key="contractions_select")
    remarques = st.text_area("Remarques ou sensations particulières (facultatif)", key="remarques_text")

    # --- Enregistrement ---
    if st.button("💾 Enregistrer", key="save_button"):
        nouvelle_obs = {
            "Date": date_jour.strftime("%Y-%m-%d"),
            "Moment": moment,
            "Fatigue": fatigue,
            "Douleurs": douleur,
            "Nausees": nausees,
            "Maux_de_tete": maux_tete,
            "RGO": rgo,
            "Sommeil": sommeil,
            "Humeur": humeur,
            "Contractions": contractions,
            "Remarques": remarques,
        }
        df = pd.concat([df, pd.DataFrame([nouvelle_obs])], ignore_index=True)
        df.to_csv(FICHIER, index=False)
        st.success("Observation enregistrée avec succès ✅")

    # --- Résumé du jour ---
    st.markdown("<h2 style='color:#B32B69;'>📊 Résumé et conseil du jour</h2>", unsafe_allow_html=True)
    if not df.empty:
        dernier = df.iloc[-1]
        score = 10 - ((dernier["Fatigue"] + dernier["Douleurs"] + dernier["Nausees"] +
                       dernier["Maux_de_tete"] + dernier["RGO"]) / 5)

        col1, col2, col3 = st.columns(3)
        col1.metric("Fatigue", f"{dernier['Fatigue']}/10")
        col2.metric("Douleurs", f"{dernier['Douleurs']}/10")
        col3.metric("Nausées", f"{dernier['Nausees']}/10")

        st.metric("Indice de bien-être global", f"{score:.1f}/10")

        if dernier["Douleurs"] >= 8 or dernier["Contractions"] == "Régulières":
            st.error("🚨 Douleurs fortes ou contractions régulières — consultez rapidement un professionnel de santé.")
        elif dernier["Fatigue"] > 7 and dernier["Nausees"] > 7:
            st.warning("⚠️ Fatigue et nausées importantes — surveillez et reposez-vous.")
        elif dernier["Maux_de_tete"] > 8 or dernier["RGO"] > 8:
            st.warning("⚠️ Symptômes intenses (maux de tête ou reflux) — surveillez et parlez-en à votre sage-femme.")
        else:
            st.success("✅ Tout semble normal aujourd’hui. Continuez à bien vous hydrater et à vous reposer.")
    else:
        st.info("Aucune donnée enregistrée pour le moment. Ajoutez une observation ci-dessus.")

    # --- Filtrage par mois ---
    st.markdown("<h2 style='color:#B32B69;'>🔎 Filtrer les données par mois</h2>", unsafe_allow_html=True)
    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"])
        mois_disponibles = sorted(df["Date"].dt.strftime("%Y-%m").unique())
        mois_selectionne = st.selectbox("Choisir un mois :", mois_disponibles,
                                        index=len(mois_disponibles)-1, key="mois_select")

        df_filtre = df[df["Date"].dt.strftime("%Y-%m") == mois_selectionne]
        st.write(f"### Données du mois : {mois_selectionne}")
        st.dataframe(df_filtre)

        fig, ax = plt.subplots()
        symptomes_a_afficher = ["Fatigue", "Douleurs", "Nausees", "Maux_de_tete", "RGO"]
        cols = [c for c in symptomes_a_afficher if c in df_filtre.columns]
        df_filtre.plot(x="Date", y=cols, ax=ax, marker="o")
        ax.set_ylabel("Niveau (0-10)")
        ax.set_title(f"Évolution des symptômes - {mois_selectionne}")
        st.pyplot(fig)
    else:
        st.info("Aucune donnée disponible pour filtrer.")

    # --- Pied de page ---
    st.markdown("<hr>", unsafe_allow_html=True)
    st.caption("👩‍💻 Développé avec ❤️ par Maddy — Projet Python SDA (Octobre 2025)")

# PAGE 2 : CONSEILS GROSSESSE

elif page == "Conseils grossesse":
    st.markdown("<h1 style='color:#B32B69;'>🌼 Conseils Bien-Être pendant la Grossesse</h1>", unsafe_allow_html=True)
    st.markdown("""
    Voici quelques conseils généraux pour mieux vivre votre grossesse 💕 :  
    <br>
    - 🥤 **Hydratez-vous** régulièrement (1,5 à 2 litres d’eau par jour).  
    - 💤 **Reposez-vous** dès que possible, surtout en fin de journée.  
    - 🚶‍♀️ **Marchez** un peu chaque jour pour favoriser la circulation.  
    - 🧘‍♀️ **Évitez le stress** : respiration, musique douce, lecture…  
    - 🍎 **Alimentation équilibrée** : fruits, légumes, protéines maigres.  
    - ☎️ **Contactez votre sage-femme** en cas de douleurs, saignements ou contractions régulières.  
    <br>
    > ⚠️ Ces conseils sont généraux et ne remplacent pas un avis médical.  
    """, unsafe_allow_html=True)

    st.markdown("<br><br><hr>", unsafe_allow_html=True)
    st.caption("🌸 Mon Assistante de Grossesse — Page conseils — Octobre 2025")
