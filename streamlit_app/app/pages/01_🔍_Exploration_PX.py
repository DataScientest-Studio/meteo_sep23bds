import streamlit as st
import io  # pour afficher la sortie de df.info()
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Prévision météo en Australie", page_icon=":partly_sunny:"
)


# = SIDEBAR =
with st.sidebar:
    st.header(":partly_sunny: Prévision météo en Australie")
    st.markdown(
        "Un projet de _data science_ réalisé par [Alexandre Winger](https://github.com/alexandrewinger) et [Omar Choa](https://www.linkedin.com/in/omarchoa/)."
    )


df = pd.read_csv("../../data/raw/weatherAUS.csv")

# Liste des variables numériques pour créer un menu déroulant pour les graphes:
var_num = list(df.select_dtypes(include=float).columns)

# Liste des stations:
liste_stations = list(df["Location"].unique())

st.title(":mag: Exploration")
st.divider()

# Tentative d'affichage de la page html "stations.html": ne marche pas.
# station_map = open("../../data/external/stations.html", "r")
# source_code = station_map.read()
# print(source_code)
# components.html(source_code)
# source_code = station_map.close()

# Affichage de la carte d'Australie avec les stations:
st.markdown(
    """Notre tableau contient des données provenant de :orange[49 stations différentes]:"""
)
st.write("\n")
gps = pd.read_excel("../../data/external/station_gps_region.xlsx")
gps.rename({"CodeRegion": "Region"}, axis=1, inplace=True)
gps["Region"].replace(
    to_replace={
        "NSW": "New South Wales",
        "ACT": "Australian Capital Territory",
        "VIC": "Victoria",
        "QLD": "Queensland",
        "SA": "South Australia",
        "WA": "Western Australia",
        "TAS": "Tasmania",
        "NT": "Northern Territory",
    },
    inplace=True,
)
fig = px.scatter_mapbox(
    data_frame=gps,
    lat="Latitude",
    lon="Longitude",
    color="Region",
    hover_name="Location",
    color_discrete_sequence=px.colors.qualitative.Vivid,
    zoom=2.5,
    mapbox_style="carto-positron",
)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
st.plotly_chart(fig)


# Présentation du tableau:
st.markdown(
    """Le tableau est constitué de :orange[relevés quotidiens] de grandeurs physiques
                mesurées :violet[par chaque station], sur une durée :blue[d'environ 10 ans, entre 2007 et 2017]."""
)
st.dataframe(df.head(10))

st.markdown(
    """Il contient environ :orange[150 000 lignes], et :violet[23 colonnes]. Le fichier fait 25.5 MB."""
)
st.write(df.shape)

st.markdown(
    """Variable cible: `RainTomorrow`. Il s'agit de prévoir s'il pleuvra le lendemain en se basant sur les mesures de la journée.
                Cette variable est :orange[déséquilibrée]: il fait beau 78 \% du temps, et il pleut les 22 \% restants."""
)

if st.checkbox("Afficher les infos"):
    st.markdown(
        """Il y a :orange[16 variables quantitatives] et :violet[7 variables qualitatives]:"""
    )
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

if st.checkbox("Afficher le pourcentage de  NaN"):
    st.markdown(
        """Certaines grandeurs sont :red[massivement absentes], comme `Evaporation` ou `Sunshine`."""
    )
    st.dataframe(df.isna().sum() / df.shape[0] * 100)
