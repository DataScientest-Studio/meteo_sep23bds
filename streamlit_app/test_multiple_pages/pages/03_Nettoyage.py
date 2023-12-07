import streamlit as st


# = TITRE =
st.title("Projet Météo en Australie")

## == PAGE ==
st.header(":broom: Nettoyage des données")

st.divider()

### === SECTION ===
st.subheader(":thinking_face: Quels choix effectuer ?")

st.markdown("Nous devons gérer des **NaN** dans :")
st.markdown("- 16 variables :violet[numériques]")
st.markdown("- 7 variables :orange[catégorielles]")

st.markdown("Nous avons identifié **deux options :**")
st.markdown("- :blue[Remplacement]")
st.markdown("- :red[Suppression]")

st.write("\n")

st.markdown(
    "Illustration avec le :blue[remplacement] des NaN dans les variables de type température (:violet[numériques]) à Melbourne :"
)
strategie_remplacement_temp = ["(aucune)", "interpolate", "mean"]
strategie_remplacement_temp_choix = st.radio(
    "Quelle stratégie de remplacement des NaN ?", strategie_remplacement_temp
)
st.image(
    "../../reports/figures/date_vs_temp_Melbourne_{}.png".format(
        strategie_remplacement_temp_choix
    )
)

st.write("\n")

st.markdown(
    "Illustration avec le :blue[remplacement] des NaN dans les variables de type vent (:violet[numériques] et :orange[catégorielles]) à Sydney :"
)
strategie_remplacement_vent = ["dropna", "fillna"]
strategie_remplacement_vent_choix = st.radio(
    "Quelle stratégie de remplacement des NaN ?", strategie_remplacement_vent
)
st.image(
    "../../reports/figures/rose_vents_Sydney_{}.png".format(
        strategie_remplacement_vent_choix
    )
)

st.write("\n")

st.markdown(
    "Illustration avec la :red[suppression] des NaN dans les variables pseudo-cible et cible (:orange[catégorielles]) :"
)
var_cible = ["RainToday", "RainTomorrow"]
var_cible_choix = st.radio("Quelle variable ?", var_cible)
strategie_remplacement_cible = ["(aucune)", "dropna"]
strategie_remplacement_cible_choix = st.radio(
    "Quelle stratégie de remplacement des NaN ?", strategie_remplacement_cible
)
st.image(
    "../../reports/figures/distrib_{}_{}.png".format(
        var_cible_choix, strategie_remplacement_cible_choix
    )
)

st.write("\n")

st.markdown("**Résumé :**")
st.markdown("- `Date` : aucune action nécessaire")
st.markdown("- `Location` : aucune action nécessaire")
st.markdown(
    "- Toutes les variables :violet[numériques] sauf `Rainfall` : :blue[remplacement] des NaN par la **moyenne** de chaque station"
)
st.markdown(
    "- `WindGustDir`, `WindDir9am`, `WindDir3pm` : :blue[remplacement] des NaN par la **mode** de chaque station"
)
st.markdown("- `RainToday`, `RainTomorrow` : :red[suppression] des NaN")


st.divider()

### === SECTION ===
st.subheader(":hammer_and_wrench: _Preprocessing_ et _feature engineering_")

st.markdown("Variables :violet[numériques] : standardisation")

st.markdown("Variables :orange[catégorielles] :")
st.markdown("- `Date` : extraction et enregistrement de l'année, mois et jour")
st.markdown("- `Location` : encodage des valeurs de `0` à `48`")
st.markdown(
    "- `WindGustDir`, `WindDir9am`, `WindDir3pm` : encodage des valeurs en radians"
)
st.markdown(
    "- `RainToday`, `RainTomorrow` : encodage des valeurs par `0` (`No`) ou `1` (`Yes`)"
)

st.divider()

### === SECTION ===
st.subheader(":ladder: Phases")

st.markdown("Phase A : travail sur neuf sous-tableaux")

st.image("../../reports/figures/data_prep_pipeline.png", output_format="PNG")
