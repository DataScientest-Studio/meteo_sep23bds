import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="bright")

import joblib

df = pd.read_csv("../../data/raw/weatherAUS.csv")

# Liste des variables numériques pour créer un menu déroulant pour les graphes:
var_num = list(df.select_dtypes(include=float).columns)

# Liste des stations:
liste_stations = list(df["Location"].unique())

st.title(":bar_chart: DataVIzualisation")
st.divider()

####################################### 1. Premières analyses et stratégie de gestion des NaN ##################################
st.header("1. Premières analyses et stratégie de gestion des NaN")
# Countplot par station:
st.markdown("""Il y a environ :orange[3000 mesures] par station:""")

fig1 = plt.figure(figsize=(20, 8))
sns.countplot(x=df["Location"])
locs, labels = plt.xticks()
plt.setp(labels, rotation=90)
st.pyplot(fig1)

st.markdown(
    """On observe des fluctuations concernant le nombre de mesures par station,
            car :red[elles n'ont pas toutes la même date de départ].
            En revanche, toutes les mesures :blue[s'arrêtent en même temps]:"""
)

# Analyse des dates
df_dates = pd.read_csv("../../data/interim/dates.csv")
st.dataframe(df_dates.head(10))

# Strip plots :
if st.checkbox("Afficher le graphique strip plot:"):
    st.markdown(
        """ Observons les strip plots de quelques grandeurs:
            """
    )

    grandeur = st.selectbox("Quelle grandeur afficher?", var_num)

    fig2 = plt.figure(figsize=(20, 8))
    sns.stripplot(
        y=df[grandeur],
        x=df["Location"],
        hue=df["RainToday"],
        size=2,
        palette=["gold", "darkturquoise"],
    )
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)
    st.pyplot(fig2)

    st.markdown(
        """On découvre ainsi que certaines stations :red[ne mesurent pas du tout
            certaines grandeurs], sans doute car elles n'ont pas le matériel adapté.
            Voilà une première piste d'explication du taux important de NaN.
            On voudrait savoir quelles sont les grandeurs non mesurées
            par une station donnée.
            """
    )

# Grandeurs non mesurées
dict = joblib.load("dict_station_non_mes.joblib")
dict_reverse = joblib.load("dict_reverse.joblib")


station = st.selectbox("Quelle station choisir?", liste_stations)
grandeurs_non_mesurees = dict[station]
st.write(
    "Ainsi, on voit que la station",
    station,
    "ne mesure pas les grandeurs:",
    grandeurs_non_mesurees,
)

st.markdown(
    """Par chance, les différentes modalités de grandeurs mesurées ne sont pas
                trop importantes: :green[il n'y en a que neuf].
            """
)

# Heatmap des nan:
nan_map = pd.read_csv("../../data/interim/nan_map.csv", index_col="Location")
fig3 = plt.figure(figsize=(20, 7))
ax = sns.heatmap(
    nan_map.T,
    annot=False,
    cmap="RdYlGn_r",
    square=True,
    linewidth=1,
    annot_kws={"size": 6},
    fmt=".0f",
    cbar_kws={"label": "Percentage"},
)

plt.title("Taux de NaN", fontweight="bold", fontsize=16)
plt.xlabel("Variable", fontweight="bold")
plt.ylabel("Location", fontweight="bold")
plt.xticks(rotation=90)
cbar_axes = ax.figure.axes[-1].yaxis.label.set_weight("bold")

st.pyplot(fig3)

# Regroupement des stations par grandeurs non mesurées:
st.markdown(
    """On peut :blue[regrouper les stations] en fonction des :orange[modalités de grandeurs non mesurées]:
            """
)
modes = list(
    dict_reverse.keys()
)  # liste des 9 modalités de non mesures concaténées (ex: Evaporation_Sunshine)
gnm = st.selectbox("Quelle modalité choisir?", modes)
st.write(dict_reverse[gnm])

# Conclusion:
st.markdown(
    """La mise en évidence de la structure du jeu de données et des valeurs manquantes nous invite à :blue[créer 9 datasets différents]
            (un par modalité de grandeurs non mesurées) pour avoir une gestion plus fine des NaN.
            Il suffira de supprimer les colonnes correspondant aux grandeurs non mesurées une fois les tableaux crées.
            """
)

# Élargissement et visualisation de la distribution spatio-temporelle des données pour des variables choisies (graphiques en « codes barre »)
st.markdown(
     """Il existe aussi une :orange[répartition des NaN plutôt aléatoire], 
     correspondant sans doute à des interruptions momentanées des appareils de mesures. 
     Nous les gérerons en remplacant ces valeurs par la valeur moyenne 
     ou la modalité la plus fréquente calculée par station au sein de chaque tableau."""
)
code_barre_var = ["Evaporation", "Sunshine", "Cloud9am", "Cloud3pm"]
code_barre_var_choix = st.selectbox("Quelle variable visualiser ?", code_barre_var)
st.image("../../reports/figures/code_barre_{}.png".format(code_barre_var_choix))

########################################### 2. Analyse de la distribution statistiques des valeurs  ##############################
st.header("2. Analyse de la distribution statistiques des valeurs")
st.markdown(
    """Nous cherchons à déterminer s'il y a des valeurs extrêmes aberrantes.
            """
)
if st.checkbox("Afficher la description statistique"):
    st.dataframe(df.describe())
st.markdown(
    """A première vue, :green[tout à l'air normal] 	:heavy_check_mark:.
            """
)

st.subheader("2.a Variables numériques")
st.markdown(
    """Vérifions -le en regardant de plus prêt la distribution des variables numériques.
            """
)

mesure = st.selectbox("Quelle grandeur numérique étudier?", var_num)

df_mes = df[mesure]
df_mes.dropna(inplace=True)

ext_min = df_mes.quantile(q=0.25) - 1.5 * (
    df_mes.quantile(q=0.75) - df_mes.quantile(q=0.25)
)
# ext_min est la frontière pour les valeurs extrèmes minimales, cad < Q1 -1.5*IQR
ext_max = df_mes.quantile(q=0.75) + 1.5 * (
    df_mes.quantile(q=0.75) - df_mes.quantile(q=0.25)
)
# ext_max est la frontière pour les valeurs extrèmes maximales, cad > Q + 1.5*IQR

df_mes_min = df_mes.loc[df_mes < ext_min]
p_min = round(df_mes_min.shape[0] / df_mes.shape[0] * 100, 2)
st.write(
    "Il y a ",
    df_mes_min.shape[0],
    ":red[valeurs extrêmes inférieures] pour la mesure",
    str(mesure),
    "sur",
    df_mes.shape[0],
    "valeurs mesurées.",
)
st.write("Cela correspond à", p_min, "% des valeurs de cette colonne.")

df_mes_max = df_mes.loc[df_mes > ext_max]
p_max = round(df_mes_max.shape[0] / df_mes.shape[0] * 100, 2)
st.write(
    "Il y a ",
    df_mes_max.shape[0],
    ":red[valeurs extrêmes supérieures] pour la mesure",
    str(mesure),
    "sur",
    df_mes.shape[0],
    "valeurs mesurées.",
)
st.write("Cela correspond à", p_max, "% des valeurs de cette colonne.")

import statsmodels.api as sm

fig4 = plt.figure(figsize=(7, 5))

plt.boxplot(df_mes)
plt.xlabel(str(mesure))
plt.ylabel("Valeurs")
plt.title("Distribution de la grandeur " + mesure)
plt.axes([0.65, 0.65, 0.2, 0.15])
plt.hist(df_mes, rwidth=0.8, color="royalblue")
plt.title("Histogramme")
# plt.xticks([])
plt.yticks([])

st.pyplot(fig4)

st.markdown(
    """ **Conclusion**: :green[Tout est en ordre], il n'y a pas de mesure particulière à prendre concernant la distribution des variables numériques.
"""
)

st.write("\n")

# Visualisation de la distribution spatiale de variables choisies (graphiques en boîtes à moustaches)
st.markdown(
    "Les variables sous étude étant des **paramètres météorologiques**, nous pourrions supposer qu’elles soient également **fonction du lieu** d’enregistrement des données ; une décomposition sur cet axe pourrait donc se révéler instructive."
)
st.markdown("Voici quelques illustrations pour les variables numériques liées au vent.")
box_plot_var = ["WindGustSpeed", "WindSpeed9am", "WindSpeed3pm"]
box_plot_var_choix = st.selectbox("Quelle variable visualiser ?", box_plot_var)
st.image("../../reports/figures/box_plot_{}.png".format(box_plot_var_choix))

### === VARIABLES CATÉGORIELLES ===

st.subheader("2.b Variables catégorielles")

st.markdown("Nous examinons ensuite les variables catégorielles.")

st.markdown(
    "Les illustrations ci-dessous présentent **les plus fortes rafales de vent (`WindGustDir`) à chaque station météorologique** sous forme de rose des vents."
)

liste_stations_choix = st.selectbox("Quelle station visualiser ?", liste_stations)
st.image("../../reports/figures/rose_vents_{}.png".format(liste_stations_choix))

st.markdown(
    "Enfin, nous concluons avec les visualisations de la pseudo-variable cible, `RainToday`, et de la variable cible, `RainTomorrow`, dont la valeur est celle de `RainToday` le jour précédent."
)

cible_var = ["`RainToday`", "`RainTomorrow`"]
cible_var_choix = st.radio("Quelle variable visualiser ?", cible_var)
st.image("../../reports/figures/distrib_{}_Aucune.png".format(cible_var_choix))
