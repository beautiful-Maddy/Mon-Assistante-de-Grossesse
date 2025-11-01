# 🤰 Mon Assistante de Grossesse

## 🌸 Objectif du projet
**Mon Assistante de Grossesse** est une application web interactive développée avec **Streamlit**.  
Elle accompagne les futures mamans au quotidien en leur permettant de :

- Suivre leurs **symptômes de grossesse** jour après jour 🩺  
- Visualiser l’évolution de leur **bien-être** 📊  
- Gérer leurs **tâches quotidiennes** 📝  
- Écrire des **notes personnelles** 🗒️  
- Chronométrer leurs **contractions** ⏱️  

## ✨ Fonctionnalités principales

| Fonctionnalité | Description |
|----------------|-------------|
| 🩺 **Suivi quotidien** | Formulaire pour enregistrer fatigue, douleurs, nausées, sommeil, humeur, etc. |
| 📊 **Visualisation mensuelle** | Graphique d’évolution des symptômes selon la période sélectionnée. |
| ✅ **To-Do List** | Gestion des tâches à faire avec ajout, suppression et validation. |
| 🗒️ **Espace de notes** | Zone libre pour noter des idées, des ressentis ou des questions à poser au médecin. |
| ⏱️ **Compteur de contractions** | Démarrage / arrêt d’un chronomètre pour suivre les durées et intervalles. |
| 💬 **Conseils grossesse** | Recommandations générales de bien-être et d’hygiène de vie. |
| 💾 **Sauvegarde CSV** | Toutes les observations sont enregistrées dans un fichier local pour consultation ultérieure. |

---

## 🖌️ Apparence et thème

L’application adopte un style doux et lisible, défini dans le fichier `.streamlit/config.toml` :

```toml
[theme]
primaryColor = "#B32B69"
backgroundColor = "#FFF8FB"
secondaryBackgroundColor = "#FCE4EC"
textColor = "#3D3D3D"
font = "sans serif"
```


## 🛠️ Technologies utilisées

- **Python 3.10+**
- **Streamlit** — Interface web interactive  
- **Pandas** — Gestion et sauvegarde des données  
- **Matplotlib** — Visualisation graphique  
- **Datetime / Time** — Gestion des dates et du timer  
- **Session State** — Persistance des données locales (To-Do, notes, historique)

---

## ⚙️ Installation et lancement

### 1️⃣ Cloner le dépôt
```bash
git clone https://github.com/<ton_nom_utilisateur>/mon-assistante-grossesse.git
cd mon-assistante-grossesse
```

2️⃣ **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3️⃣ **Lancer l’application**
```bash
streamlit run app.py
```

4️⃣ **Ouvrir le navigateur**
> 👉 L’application s’ouvre automatiquement sur :  
> [http://localhost:8501](http://localhost:8501)

---

## 📁 Structure du projet

```
mon-assistante-grossesse/
│
├── app.py                         # Script principal Streamlit
├── requirements.txt               # Liste des dépendances
├── data/
│   └── suivi_grossesse.csv        # Sauvegarde des entrées du formulaire
├── .streamlit/
│   └── config.toml                # Fichier de thème et mise en page
└── README.md                      # Documentation du projet
```

---

## 🧠 Organisation du code

Le code est structuré en **trois grandes sections** selon la page affichée :

1️⃣ **Suivi quotidien**
   - Formulaire Streamlit pour saisir les symptômes
   - Calcul du score de bien-être
   - Enregistrement automatique dans un CSV
   - Visualisation des tendances mensuelles

2️⃣ **To-Do & Notes**
   - Gestion dynamique avec `st.session_state`
   - To-do list : ajout / suppression
   - Espace de notes : sauvegarde et affichage
   - Compteur de contractions : enregistre début, fin et durée, avec affichage en temps réel


3️⃣ **Conseils grossesse**
   - Texte statique en Markdown avec recommandations générales

---

## 📹 Vidéo de démonstration

Une **vidéo de démonstration (2 à 4 minutes)** est disponible sur Google Drive :  
🎥 [Lien vers la vidéo](https://drive.google.com/) *(à compléter après l’envoi)*

La vidéo présente :
- Le **but du projet**
- Une **démonstration complète** de l’application (formulaire → résultats)
- Une **explication du code** et de sa structure

---

## ⚠️ Avertissement

> ⚕️ Cette application est un **outil éducatif et de suivi personnel**.  
> Elle **ne remplace pas un avis médical**.  
> En cas de symptômes inhabituels, il est conseillé de consulter un professionnel de santé.

---

## 👩‍💻 Auteur

- **Nom :** Maddy et Norma  
- **Date :** Octobre 2025  

---

💗 *“Mon Assistante de Grossesse” — Un projet bienveillant pour accompagner les futures mamans, pas à pas.*
