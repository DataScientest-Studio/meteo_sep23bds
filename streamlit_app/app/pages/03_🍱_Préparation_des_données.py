import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Prévision météo en Australie", page_icon=":partly_sunny:"
)


# = SIDEBAR =
with st.sidebar:
    st.header(":partly_sunny: Prévision météo en Australie")
    st.markdown(
        "Un projet de _data science_ réalisé par [Omar CHOA](https://www.linkedin.com/in/omarchoa/) et [Alexandre WINGER](https://github.com/alexandrewinger)."
    )


tab_1, tab_2, tab_3 = st.tabs(
    [
        ":thinking_face: **Quels choix effectuer ?**",
        ":hammer_and_wrench: **_Preprocessing_ et _feature engineering_**",
        ":calendar: **Phases**",
    ]
)


with tab_1:
    # = PAGE =
    st.title(":bento: Préparation des données")

    ## == SECTION ==
    st.header(":thinking_face: Quels choix effectuer ?")

    st.write("\n")

    ### === SOUS-SECTION ===
    st.subheader("Contexte")

    st.markdown("Nous devons gérer des **NaN** dans :")
    st.markdown("- 16 variables :violet[numériques]")
    st.markdown("- 7 variables :orange[catégorielles]")

    st.markdown("Nous avons identifié **2 options :**")
    st.markdown("- :blue[Remplacement]")
    st.markdown("- :red[Suppression]")

    st.write("\n")

    ### === SOUS-SECTION ===
    st.subheader("Illustration")

    st.markdown(
        ":blue[Remplacement] des NaN dans les variables de température (:violet[numériques]) à Melbourne :"
    )
    strategie_remplacement_temp = ["Aucune", "`interpolate`", "`mean`"]
    strategie_remplacement_temp_choix = st.radio(
        "Stratégie :", strategie_remplacement_temp
    )
    st.image(
        "../../reports/figures/date_vs_temp_Melbourne_{}.png".format(
            strategie_remplacement_temp_choix
        )
    )

    st.write("\n")

    ### === SOUS-SECTION ===
    st.subheader("Illustration")

    st.markdown(
        ":blue[Remplacement] des NaN dans les variables de vent (:violet[numériques] et :orange[catégorielles]) à Sydney :"
    )
    strategie_remplacement_vent = ["`dropna`", "`fillna`"]
    strategie_remplacement_vent_choix = st.radio(
        "Stratégie :", strategie_remplacement_vent
    )
    st.image(
        "../../reports/figures/rose_vents_Sydney_{}.png".format(
            strategie_remplacement_vent_choix
        ),
        width=450,
    )

    st.write("\n")

    ### === SOUS-SECTION ===
    st.subheader("Illustration")

    st.markdown(
        ":red[Suppression] des NaN dans les variables pseudo-cible et cible (:orange[catégorielles]) :"
    )
    strategie_remplacement_cible = ["Aucune", "`dropna`"]
    strategie_remplacement_cible_choix = st.radio(
        "Stratégie :", strategie_remplacement_cible
    )
    col_1, col_2 = st.columns(2)
    with col_1:
        st.image(
            "../../reports/figures/distrib_`RainToday`_{}.png".format(
                strategie_remplacement_cible_choix
            )
        )
    with col_2:
        st.image(
            "../../reports/figures/distrib_`RainTomorrow`_{}.png".format(
                strategie_remplacement_cible_choix
            )
        )

    st.write("\n")

    ### === SOUS-SECTION ===
    st.subheader("Résumé")

    st.markdown("- `Date` : aucune action nécessaire")
    st.markdown("- `Location` : aucune action nécessaire")
    st.markdown(
        "- Toutes les variables :violet[numériques] sauf `Rainfall` : :blue[remplacement] des NaN par la **moyenne** de chaque station"
    )
    st.markdown(
        "- `WindGustDir`, `WindDir9am`, `WindDir3pm` : :blue[remplacement] des NaN par la **mode** de chaque station"
    )
    st.markdown("- `RainToday`, `RainTomorrow` : :red[suppression] des NaN")


with tab_2:
    # = PAGE =
    st.title(":bento: Préparation des données")

    ## == SECTION ==
    st.header(":hammer_and_wrench: _Preprocessing_ et _feature engineering_")

    st.write("\n")

    ### === SOUS-SECTION ===
    st.subheader("Variables :violet[numériques]")

    st.markdown("- Standardisation")

    st.write("\n")

    ### === SOUS-SECTION ===
    st.subheader("Variables :orange[catégorielles]")

    st.markdown("- `Date` : extraction et enregistrement de l'année, mois et jour")
    st.markdown("- `Location` : encodage des valeurs de `0` à `48`")
    st.markdown(
        "- `WindGustDir`, `WindDir9am`, `WindDir3pm` : encodage des valeurs en radians"
    )
    st.markdown(
        "- `RainToday`, `RainTomorrow` : encodage des valeurs par `0` (`No`) ou `1` (`Yes`)"
    )


with tab_3:
    # = PAGE =
    st.title(":bento: Préparation des données")

    ## == SECTION ==
    st.header(":calendar: Phases")

    st.write("\n")

    ### === SOUS-SECTION ===
    st.subheader("Phase A")

    st.markdown("Travail sur **9 sous-tableaux**")

    components.html(
        html="""<iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="800" height="450" src="https://www.figma.com/embed?embed_host=share&url=https%3A%2F%2Fwww.figma.com%2Ffile%2F8aPx8akpCF1HLdDkNdv7Nz%2Fpipeline%3Ftype%3Dwhiteboard%26node-id%3D0%253A1%26t%3DitCNIBp3Eo7fHMvB-1" allowfullscreen></iframe>""",
        width=800,
        height=450,
    )

    st.write("\n")

    ### === SOUS-SECTION ===
    st.subheader("Phase B")

    st.markdown("Retour à **1 tableau unique**")

    components.html(
        html="""<iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="640" height="480" src="https://www.figma.com/embed?embed_host=share&url=https%3A%2F%2Fwww.figma.com%2Ffile%2FxnhjGD3NKTM5TSNEoOQmc0%2Fdata_prep_pipeline_1df%3Ftype%3Dwhiteboard%26node-id%3D0%253A1%26t%3DVPZbJJ5vB8r7ow4q-1" allowfullscreen></iframe>""",
        width=640,
        height=480,
    )

    st.write("\n")

    ### === SOUS-SECTION ===
    st.subheader("Phase C")

    st.markdown("Choix de **métrique** et **optimisation**")
    st.markdown("- **Objectif :** 5 prédictions justes sur 6 (83%)")
    st.markdown(
        "- **Implémentation :** évaluation souple de `accuracy`, `precision` et `recall`"
    )
    st.markdown(
        "- **Optimisation :** stratification, rééchantillonnage, standardisation"
    )
