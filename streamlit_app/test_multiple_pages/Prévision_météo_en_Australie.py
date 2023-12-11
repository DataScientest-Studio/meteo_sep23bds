import streamlit as st


st.set_page_config(
    page_title="Prévision météo en Australie", page_icon=":partly_sunny:"
)


# = PAGE =
st.title(":partly_sunny: Prévision météo en Australie")


## == SECTION ==
st.header(":wave: Bienvenue !")

st.markdown(
    "Cette application Streamlit présente le :red[projet fil rouge] que nous avons réalisé dans le cadre de notre formation « [Data Scientist](https://datascientest.com/formation-data-scientist) » chez [DataScientest](https://datascientest.com/)."
)

st.markdown(
    "Notre projet est issu de « [Rain in Australia](https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package) », une compétition [Kaggle](https://www.kaggle.com/) qui propose un ensemble de relevés météorologiques contenant environ 10 ans d’observations enregistrées par 49 stations en Australie."
)

st.markdown(
    "Notre :red[objectif] reprend celui de la compétition Kaggle : développer, à partir des données, un modèle de classification visant à prédire s'il pleuvra le lendemain ou pas."
)

## == SECTION ==
st.header(":technologist::technologist: Auteurs")

st.markdown("Nous sommes Alex et Omar, les **Weather Boys** !")

st.markdown(
    "Tous deux issus d'un parcours scientifique et attirés par le monde de la _data_, nous avons décidé de sauter le pas en nous inscrivant chez DataScientest."
)

st.markdown("Cliquez sur les liens suivants pour en savoir plus sur nous !")
st.markdown("- [Alexandre Winger](https://github.com/alexandrewinger)")
st.markdown("- [Omar Choa](https://www.linkedin.com/in/omarchoa/)")
