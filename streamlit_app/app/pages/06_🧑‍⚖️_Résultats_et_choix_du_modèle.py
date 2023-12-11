import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="bright")


st.set_page_config(
    page_title="Prévision météo en Australie", page_icon=":partly_sunny:"
)


# = SIDEBAR =
with st.sidebar:
    st.header(":partly_sunny: Prévision météo en Australie")
    st.markdown(
        "Un projet de _data science_ réalisé par [Alexandre WINGER](https://github.com/alexandrewinger) et [Omar CHOA](https://www.linkedin.com/in/omarchoa/)."
    )


df_tot = pd.read_excel(
    "../../references/scores.xlsx"
)  # les résultats des 70+ expériences
df = pd.read_csv(
    "../../references/final_results.csv"
)  # uniquement les résultats sur le tableau entier
df_tot.drop(columns="experiment", inplace=True)

st.title(":scales: Résultats et choix du modèle")
st.divider()

if st.checkbox("Les résultats au complet:"):
    st.markdown(
        """Ce tableau reprend l':blue[ensemble des expériences réalisées], sur les 9 sous datasets, et sur le tableau entier."""
    )
    st.dataframe(df_tot)

if st.checkbox("Les résultats sur le tableau entier uniquement"):
    st.markdown(
        """Voici uniquement les résultats obtenus sur le :blue[tableau entier], avec une autre modalité de gestion des valeurs manquantes."""
    )
    st.dataframe(df)
st.markdown(
    """ En l'absence de contexte professionnel  fournissant un cahier des charges déterminé, nous choisissons un :blue[critère basé sur l'accuracy].
           A l'usage, il s'est avéré que c'était l'indicateur que nous regardions en premier. Nous pensons fournir un algorithme qui puisse prédire correctement
            le temps du lendemain :orange[5 fois sur 6], soit une accuracy de :violet[83% minimum].
            """
)

st.markdown(
    """Affichage des 10 meilleurs modèles sur le tableau entier:
            """
)
n = st.slider("n", 1, 10)
data = df.T.reset_index().copy()
fig_06_01 = plt.figure(figsize=(20, 10))
for i in list(data.columns[1 : n + 1]):  #
    plt.plot(
        data["index"][2:], data[i][2:], label=data[i][0] + " " + data[i][1], marker="*"
    )
plt.legend()
plt.xticks(rotation=90)
st.pyplot(fig_06_01)

st.markdown(
    """ Il y plusieurs candidats possibles. Notre choix final s'effectue en prenant en compte d'autres aspect, comme l'équilibre des précisions et le rappel,
            surtout pour la classe positive, minoritaire.
            **Conclusion** : Nous optons pour `RandomForest`, ré-équilibré avec SMOTE, avec un :green[seuil optimisé] grâce à la coure ROC.
            """
)
