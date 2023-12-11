import streamlit as st
import streamlit.components.v1 as components  # pour afficher un fichier html

# from PIL import Image # pour afficher des images
import io  # pour afficher la sortie de df.info()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="bright")

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
import joblib


st.set_page_config(
    page_title="Prévision météo en Australie", page_icon=":partly_sunny:"
)


df = pd.read_csv("../../data/raw/weatherAUS.csv")

# Liste des variables numériques pour créer un menu déroulant pour les graphes:
var_num = list(df.select_dtypes(include=float).columns)

# Liste des stations:
liste_stations = list(df["Location"].unique())

tab_1, tab_2, tab_3 = st.tabs(
    [
        "Ré-équilibrage",
        "Choix d'un modèle",
        "Optimisations",
    ]
)

###################################### Page modélisation #######################################
with tab_1:
    # = PAGE =
    st.title(":computer: Premières modélisations")

    ## == SOUS-SECTION ==
    st.header("Ré-équilibrage des classes")

    st.markdown(
        """ Notre variable cible est :red[très déséquilibrée]: il ne pleut pas souvent en Australie, :blue[environ 22 % du temps] seulement."""
    )
    data = pd.read_csv("../../data/processed/model_weatherAUS.csv")

    fig04_01 = plt.figure(figsize=(8, 8))
    sns.countplot(x=df["RainTomorrow"])
    st.pyplot(fig04_01)

    st.markdown(
        """ Nous choississons donc de procéder à un :blue[ré-échantillonnage des données]. Reste à savoir quelle méthode est la plus adaptée à notre problème:
                le :violet[sur-échantillonage] ou le :orange[sous-échantillonnage].
                Nous testerons deux algorithmes: :violet[SMOTE] et :orange[ClusterCentroids]."""
    )

    ## == SOUS-SECTION ==
    st.header("Modèles de classification simples")

    st.markdown(
        """ On choisit d'entrainer 4 modèles :
                        * Régression Logistique (logreg),
                        * Arbre de décision (Decision Tree, dt),
                        * Forêts aléatoires (RandomForest, rdf),
                        * K plus proches voisins (K Nearest Neighbors, knn)"""
    )

    st.markdown(
        """ Pour chaque modèle, une sélection des meilleurs paramètres est effectuée grâce à `GridSearchCV`.
                Nous entrainons chaque modèle sur l'ensemble :violet[SMOTE] ou :orange[ClusterCentroids], et nous affichons les résultats sur les ensembles d':blue[entrainement] et de :green[test]:
            """
    )
    df_report = pd.read_csv("../../models/saves/reports/report.csv")
    df_report.drop(columns="Unnamed: 0", inplace=True)
    st.dataframe(df_report.head(16))

    fig04_02 = plt.figure(figsize=(8, 8))
    sns.barplot(data=df_report, x="Modele", y="f1_macro_avg", hue="Sampling")
    plt.title(
        "Mesure de f1 moyen pour les différents modèles optimisés sur le tableau complet"
    )
    st.pyplot(fig04_02)

    st.markdown(
        """ **Conclusion** : Le ré-échantillonage SMOTE donne :green[toujours de meilleurs résultats] que ClusterCentroids,
                nous le choisirons pour le reste des modèles.
                """
    )

with tab_2:
    # = PAGE =
    st.title(":computer: Premières modélisations")

    ## == SOUS-SECTION ==
    st.header("Choisir un modèle")

    st.markdown(
        """ Regardons à présent plus en détail le f1-score pour chacun des modèles:
                """
    )
    df_report_bis = df_report.loc[df_report["Sampling"] == "SMOTE"].copy()

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("f1-score")

    sns.barplot(
        ax=axes[0],
        data=df_report_bis,
        x="Modele",
        y="f1_macro_avg",
        hue="Evaluation",
        palette=["lightgrey", "darkgrey"],
    )
    axes[0].set_title("Moyenne f1")

    sns.barplot(
        ax=axes[1],
        data=df_report_bis,
        x="Modele",
        y="f1_0",
        hue="Evaluation",
        palette=["palegoldenrod", "gold"],
    )
    axes[1].set_title("f1_0 sur la classe négative: pas de pluie")

    sns.barplot(
        ax=axes[2],
        data=df_report_bis,
        x="Modele",
        y="f1_1",
        hue="Evaluation",
        palette=["paleturquoise", "darkturquoise"],
    )
    axes[2].set_title("f1_1 sur la classe positive: pluie demain")

    st.pyplot(fig)

    st.markdown(
        """ **Conclusion** : Rdf est :green[notre meilleur modèle] parmi les 4,
                mais il présente un :red[certain overfitting]. On constate aussi un :red[certain déséquilibre] dans la qualité des prédictions sur les classes positives et négatives.
                """
    )

with tab_3:
    # = PAGE =
    st.title(":computer: Premières modélisations")

    ## == SOUS-SECTION ==
    st.header(
        "Réduire l'overfitting sur RdF pour réduire l'écart de qualité des prédictions?"
    )

    st.markdown(
        """ Tentons de réduire l'overfitting sur RdF en faisant de la feature selection.
                """
    )
    feature_importance = pd.read_csv(
        "../../models/saves/reports/rdf_feats_importances.csv"
    ).sort_values(by="Importance", ascending=False)

    fig_04_03 = plt.figure(figsize=(8, 8))
    sns.barplot(data=feature_importance, y="Feature", x="Importance", color="darkblue")
    plt.title("Feature importances sur RdF")
    st.pyplot(fig_04_03)

    st.markdown(
        """Pour cela, on enlève au fur et à mesure les features de moindre importances
                pour tenter de chercher un optimum. On obtient la courbe suivante:
                """
    )

    df_f1 = pd.read_csv("../../models/saves/reports/rdf_feats_removed.csv")

    fig_04_04 = plt.figure(figsize=(8, 8))
    sns.lineplot(
        data=df_f1, x="NFeatsRemoved", y="f1_0_test", label="f1_0_test", c="gold"
    )
    sns.lineplot(
        data=df_f1,
        x="NFeatsRemoved",
        y="f1_1_test",
        label="f1_1_test",
        c="darkturquoise",
    )
    sns.lineplot(
        data=df_f1,
        x="NFeatsRemoved",
        y="f1_0_train",
        label="f1_0_train",
        c="gold",
        linestyle="dotted",
    )
    sns.lineplot(
        data=df_f1,
        x="NFeatsRemoved",
        y="f1_1_train",
        label="f1_1_train",
        c="darkturquoise",
        linestyle="dotted",
    )
    plt.ylim([0, 1.2])
    plt.ylabel("f1 score")
    plt.title(
        "Evolution du f1 score de RdF en fonction du nombre de variables enlevées"
    )
    plt.legend()
    st.pyplot(fig_04_04)

    st.markdown(
        """ **Conclusion:** :red[Ce n'est pas le résultat que nous espérions]: il n'y a pas d'amélioration du f1-score ni de réduction d'overfitting en faisant de la feature selection sur ce modèle.
                """
    )

    ## == SOUS-SECTION ==
    st.header("Un premier bilan:")

    st.markdown(
        """ Pour tenter de rééquilibrer la qualité de prédiction entre les deux classes, on effectue une :blue[recherche de meilleur seuil] grâce à une courbe ROC.
                """
    )

    st.image("../../references/rdf_roc.jpg")

    st.markdown(
        """ **Conclusion:**
                C'est le :green[meilleur modèle que nous obtenons] jusqu'à présent.
                Il donne des bonnes prédictions dans 6 cas sur 7 :dart:.
                Cependant, il reste un :red[déséquilibre de qualité de prédiction] entre les classes.
                De plus, le :orange[recall de la classe positive n'est pas bon]: il classe la moitité des journées de pluie dans les deux catégories de prédictions.
                """
    )
