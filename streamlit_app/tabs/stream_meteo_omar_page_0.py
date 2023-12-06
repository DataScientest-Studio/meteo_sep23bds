import pandas as pd
import streamlit as st
import io


df = pd.read_csv("../../data/raw/weatherAUS.csv")


def page_1():
    st.write("### Introduction")

    # Tentative d'affichage de la page html "stations.html": ne marche pas.
    # station_map = open("../../data/external/stations.html", "r")
    # source_code = station_map.read()
    # print(source_code)
    # components.html(source_code)
    # source_code = station_map.close()

    # Affichage de la carte d'Australie avec les stations:
    st.markdown(
        """Notre tableau contient des données provenant de 49 stations différentes:"""
    )
    image = "../../data/external/carte_stations.jpg"
    st.image(image, caption="Carte des stations")

    # Présentation du tableau:
    st.markdown(
        """Le tableau est constitué de relevés quotidiens de grandeurs physiques
                mesurées par chaque station, sur une durée d'environ 10 ans, entre 2007 et 2017."""
    )
    st.dataframe(df.head(10))

    st.markdown(
        """Il contient environ 150 000 lignes, et 23 colonnes. Le fichier fait 25.5 MB."""
    )
    st.write(df.shape)

    st.markdown(
        """Variable cible: `RainTomorrow`. Il s'agit de prévoir s'il pleuvra le lendemain en se basant sur les mesures de la journée.
                Cette variable est déséquilibrée: il fait beau 78 \% du temps, et il pleut les 22 \% restants."""
    )

    if st.checkbox("Afficher les infos"):
        st.markdown(
            """Il y a 16 variables quantitatives et 7 variables qualitatives:"""
        )
        buffer = io.StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)

    if st.checkbox("Afficher le pourcentage de  NaN"):
        st.markdown(
            """Certaines grandeurs sont massivement absentes, comme `Evaporation` ou `Sunshine`."""
        )
        st.dataframe(df.isna().sum() / df.shape[0] * 100)

    return
