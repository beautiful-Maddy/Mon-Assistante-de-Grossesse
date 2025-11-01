import streamlit as st
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt

# Configuration de la page 
st.set_page_config(page_title="Mon Assistante de Grossesse", 
                   page_icon="🤰", 
                   layout="centered"
                   )

# Navigation
page = st.sidebar.selectbox(
    "📋 Navigation",
    ["Suivi quotidien", "To-Do & Notes", "Conseils grossesse"],
    key="nav_page"
)


# Données
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

    # Saisie utilisateur
    st.markdown("<h2 style='color:#B32B69;'>🩺 Enregistrer une observation</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        moment = st.selectbox("Moment de la journée", ["Matin", "Soir"], key="moment_select")
        date_jour = st.date_input("Date du jour", date.today(), key="date_input")

    with col2:
        fatigue = st.slider("💤 Niveau de fatigue", 0, 10, 5, key="fatigue_slider")
        douleur = st.slider("💢 Douleurs corporelles (dos, bassin, jambes…)", 0, 10, 3, key="douleur_slider")

    # Bloc explicatif global
    st.progress(0)
    st.caption("🔹 0 = aucun symptôme  |  🔸 5 = modéré  |  🔺 10 = très intense")

    # Symptômes détaillés
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

    # Enregistrement
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

    #  Résumé du jour
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
        if score >= 8:
            st.success(f"💚 Bien-être global excellent ({score:.1f}/10)")
        elif score >= 5:
            st.warning(f"🟡 Bien-être global moyen ({score:.1f}/10)")
        else:
            st.error(f"🔴 Bien-être global faible ({score:.1f}/10)")

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

    #  Filtrage par mois
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

    #  Pied de page
    st.markdown("<hr>", unsafe_allow_html=True)
    st.caption("🌸 Mon Assistante de Grossesse — Page 📅 Suivi quotidien—")

# PAGE 2 : TO-DO LIST / NOTES / COMPTEUR DE CONTRACTIONS

elif page == "To-Do & Notes":
    import datetime as dt
    import time

    st.markdown("<h1 style='color:#B32B69;'>🗒️ Organisation et suivi personnel</h1>", unsafe_allow_html=True)

    # --- TO-DO LIST ---
    st.markdown("---")
    st.header("✅ Ma To-Do List")

    # Initialisation du state
    if "todos" not in st.session_state:
        st.session_state.todos = []

    # Fonctions de callback
    def add_todo():
        task = st.session_state.new_todo.strip()
        if task:
            st.session_state.todos.append({"task": task, "done": False})
            st.session_state.new_todo = ""

    def complete_todo(index):
        st.session_state.todos[index]["done"] = not st.session_state.todos[index]["done"]

    def delete_todo(index):
        del st.session_state.todos[index]

    # Formulaire d'ajout
    with st.form("todo_form", clear_on_submit=True):
        st.text_input("Nouvelle tâche :", key="new_todo", placeholder="Entrez votre tâche ici...", label_visibility="collapsed")
        st.form_submit_button("Ajouter la tâche", on_click=add_todo)

    st.markdown("---")
    st.subheader("Tâches à faire")

    if st.session_state.todos:
        for index, todo in enumerate(st.session_state.todos):
            col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
            with col1:
                is_done = st.checkbox("", value=todo["done"], key=f"check_{index}", on_change=complete_todo, args=(index,), label_visibility="collapsed")
            with col2:
                if is_done:
                    st.markdown(f"<span style='text-decoration: line-through; color: gray;'>{todo['task']}</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"**{todo['task']}**")
            with col3:
                st.button("❌ Supprimer", key=f"delete_{index}", on_click=delete_todo, args=(index,))
    else:
        st.info("Votre liste de tâches est vide. Ajoutez une tâche ci-dessus !")

    # --- NOTES ---
    st.markdown("---")
    st.header("🗒️ Espace de notes")

    if 'notes' not in st.session_state:
        st.session_state.notes = []
    if 'current_note' not in st.session_state:
        st.session_state.current_note = ""

    def add_note():
        new_note = st.session_state.note_input.strip()
        if new_note:
            st.session_state.notes.insert(0, new_note)
            st.session_state.current_note = ""

    def delete_note(index_to_delete):
        del st.session_state.notes[index_to_delete]

    st.subheader("Ici vous pouvez écrire des informations à retenir ou des questions à poser au médecin")
    st.text_area("Écrivez votre nouvelle note ici :", key='note_input', height=150, placeholder="Saisissez votre note...", value=st.session_state.current_note)
    st.button("Ajouter la Note", on_click=add_note)

    st.markdown("---")
    st.subheader(f"Mes Notes ({len(st.session_state.notes)})")

    if st.session_state.notes:
        for i, note in enumerate(st.session_state.notes):
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.info(note)
            with col2:
                st.button("Supprimer", key=f"delete_btn_{i}", on_click=delete_note, args=(i,))
    else:
        st.write("Aucune note pour l'instant. Ajoutez-en une !")

    # --- COMPTEUR DE CONTRACTIONS ---
    st.markdown("---")
    st.header("🤰 Compteur de Contractions")

    def start_contraction():
        st.session_state.current_start_time = dt.datetime.now()
        st.session_state.is_counting = True
        st.session_state.current_end_time = None 

    def end_contraction():
        if st.session_state.is_counting and st.session_state.current_start_time is not None:
            st.session_state.current_end_time = dt.datetime.now()
            duration = st.session_state.current_end_time - st.session_state.current_start_time
            st.session_state.history.insert(0, {
                "Début (Date et Heure)": st.session_state.current_start_time.strftime("%d/%m/%Y %H:%M:%S"),
                "Fin (Heure)": st.session_state.current_end_time.strftime("%H:%M:%S"),
                "Durée (sec)": round(duration.total_seconds(), 1)
            })
            st.session_state.is_counting = False
            st.session_state.current_start_time = None
            st.session_state.current_end_time = None

    def reset_history():
        st.session_state.history = []
        st.session_state.is_counting = False
        st.session_state.current_start_time = None
        st.session_state.current_end_time = None

    # Initialisation session_state
    for key, val in {
        "is_counting": False,
        "current_start_time": None,
        "current_end_time": None,
        "history": []
    }.items():
        st.session_state.setdefault(key, val)

    col_start, col_end = st.columns(2)
    with col_start:
        st.button("🔴 Début Contraction", on_click=start_contraction, disabled=st.session_state.is_counting, use_container_width=True)
    with col_end:
        st.button("🟢 Fin Contraction", on_click=end_contraction, disabled=not st.session_state.is_counting, use_container_width=True)

    st.markdown("---")

    if st.session_state.is_counting:
        st.success(f"Contraction en cours, débutée à : **{st.session_state.current_start_time.strftime('%H:%M:%S')}**")
        placeholder = st.empty()
        elapsed = 0
        while st.session_state.is_counting:
            elapsed = int((dt.datetime.now() - st.session_state.current_start_time).total_seconds())
            placeholder.metric("Durée de la contraction actuelle", f"{elapsed} secondes")
            time.sleep(0.5)

    st.subheader(f"Historique détaillé ({len(st.session_state.history)} contractions)")
    if st.session_state.history:
        df_history = pd.DataFrame(st.session_state.history)
        st.dataframe(df_history, use_container_width=True, hide_index=True)
        st.button("Effacer l'historique", on_click=reset_history, type="secondary")
    else:
        st.info("L'historique est vide.")

    st.markdown("<br><br><hr>", unsafe_allow_html=True)
    st.caption("🌸 Mon Assistante de Grossesse — Page ✅ To-Do & Notes  —")


# PAGE 3 : CONSEILS GROSSESSE 

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
    st.caption("🌸 Mon Assistante de Grossesse — Page 🌼 conseils —")
