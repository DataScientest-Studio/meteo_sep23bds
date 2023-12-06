import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style = "whitegrid", palette = "bright")

import joblib

df = pd.read_csv("../../data/raw/weatherAUS.csv")

# Liste des variables numériques pour créer un menu déroulant pour les graphes:
var_num = list(df.select_dtypes(include = float).columns)

# Liste des stations:
liste_stations = list(df['Location'].unique())

st.title("Projet Météo en Australie")

####################################### 1. Premières analyses et stratégie de gestion des NaN ##################################
st.header("1. Premières analyses et stratégie de gestion des NaN")
# Countplot par station:
st.markdown("""Il y a environ 3000 mesures par station:""")

fig1 = plt.figure(figsize = (20, 8))
sns.countplot(x = df['Location'])
locs, labels = plt.xticks()
plt.setp(labels, rotation=90)
st.pyplot(fig1)

st.markdown("""On observe des fluctuations concernant le nombre de mesures par station, 
            car elles n'ont pas toutes la même date de départ. 
            En revanche, toutes les mesures s'arrêtent en même temps:""")

# Analyse des dates
df_dates = pd.read_csv("../../data/interim/dates.csv")
st.dataframe(df_dates.head(10))

# Strip plots : 
if st.checkbox("Afficher le graphique strip plot:"):
    st.markdown(""" Observons les strip plots de quelques grandeurs:
            """)

    grandeur = st.selectbox("Quelle grandeur afficher?" , var_num)

    fig2 = plt.figure(figsize=(20, 8))
    sns.stripplot(y = df[grandeur], x = df['Location'], hue = df['RainToday'], size = 2, palette=['gold', 'darkturquoise'])
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)
    st.pyplot(fig2)

    st.markdown("""On découvre ainsi que certaines stations ne mesurent pas du tout 
            certaines grandeurs, sans doute car elles n'ont pas le matériel adapté. 
            Voilà une première piste d'explication du taux important de NaN.  
            On voudrait savoir quelles sont les grandeurs non mesurées 
            par une station donnée.
            """)

# Grandeurs non mesurées
dict = joblib.load("dict_station_non_mes.joblib")
dict_reverse = joblib.load("dict_reverse.joblib")


station = st.selectbox("Quelle station choisir?" , liste_stations)
grandeurs_non_mesurees = dict[station]
st.write("Ainsi, on voit que la station", station, "ne mesure pas les grandeurs:", grandeurs_non_mesurees)

st.markdown("""Par chance, les différentes modalités de grandeurs mesurées ne sont pas
                trop importantes: elles sont au nombre de 9 "seulement".
            """)

# Heatmap des nan:
nan_map = pd.read_csv("../../data/interim/nan_map.csv", index_col='Location')
fig3 = plt.figure(figsize=(20, 7))
ax = sns.heatmap(nan_map.T, annot = False, cmap = "RdYlGn_r", square = True, linewidth = 1, annot_kws={"size":6}, fmt=".0f", cbar_kws = {"label": "Percentage"})

plt.title("Taux de NaN", fontweight = "bold", fontsize = 16)
plt.xlabel("Variable", fontweight = "bold")
plt.ylabel("Location", fontweight = "bold")
plt.xticks(rotation = 90)
cbar_axes = ax.figure.axes[-1].yaxis.label.set_weight("bold");

st.pyplot(fig3)

# Regroupement des stations par grandeurs non mesurées:
st.markdown("""On peut regrouper les stations en fonction des modalités de grandeurs non mesurées:
            """)
modes = list(dict_reverse.keys())     # liste des 9 modalités de non mesures concaténées (ex: Evaporation_Sunshine)
gnm = st.selectbox("Quelle modalité choisir?" , modes)
st.write(dict_reverse[gnm])

# Conclusion:
st.markdown("""La mise en évidence de la structure du jeu de données et des valeurs manquantes nous invite à créer 9 datasets différents 
            (un par modalité de grandeurs non mesurées) pour avoir une gestion plus fine des NaN. 
            Il suffira de supprimer les colonnes correspondant aux grandeurs non mesurées une fois les tableaux crées.
            """)

# Elargissement: 
st.markdown("""Il existe aussi une répartition des NaN plutôt aléatoire, correspondant sans doute à des interruptions momentannées des appareils de mesures. 
            Nous les gérerons en remplacant ces valauers par la valeur moyenne (ou la modalité la plus fréquente) 
            calculée par station au sein de chaque tableau.
            """)
# TODO: insérer le plot code barre d'Omar.

########################################### 2. Analyse de la distribution statistiques des valeurs  ##############################
st.header("2. Analyse de la distribution statistiques des valeurs")
st.markdown("""Nous cherchons à déterminer s'il y a des valeurs extrêmes aberrantes.
            """)
if st.checkbox("Afficher la description statistique"):
    st.dataframe(df.describe())
st.markdown("""A première vue, tout à l'air normal. 
            """)

st.subheader("2.a Variables numériques")
st.markdown("""Vérifions -le en regardant de plus prêt la distribution des variables numériques. 
            """)

mesure = st.selectbox("Quelle grandeur numérique étudier?" , var_num)

df_mes = df[mesure]
df_mes.dropna(inplace = True)

ext_min = df_mes.quantile(q = 0.25)-1.5*(df_mes.quantile(q = 0.75)-df_mes.quantile(q = 0.25))
# ext_min est la frontière pour les valeurs extrèmes minimales, cad < Q1 -1.5*IQR
ext_max = df_mes.quantile(q = 0.75)+1.5*(df_mes.quantile(q = 0.75)-df_mes.quantile(q = 0.25))
# ext_max est la frontière pour les valeurs extrèmes maximales, cad > Q + 1.5*IQR

df_mes_min = df_mes.loc[df_mes < ext_min]
p_min = round(df_mes_min.shape[0]/df_mes.shape[0]*100, 2)
st.write("Il y a ", df_mes_min.shape[0], "valeurs extrêmes inférieures pour la mesure", str(mesure),  "sur", df_mes.shape[0], "valeurs mesurées.")
st.write("Cela correspond à",p_min , "% des valeurs de cette colonne.")

df_mes_max = df_mes.loc[df_mes > ext_max]
p_max = round(df_mes_max.shape[0]/df_mes.shape[0]*100, 2)
st.write("Il y a ", df_mes_max.shape[0], "valeurs extrêmes inférieures pour la mesure" , str(mesure),  "sur", df_mes.shape[0], "valeurs mesurées.")
st.write("Cela correspond à",p_max , "% des valeurs de cette colonne.")

import statsmodels.api as sm
fig4 = plt.figure(figsize=(7,5))

plt.boxplot(df_mes)
plt.xlabel(str(mesure))
plt.ylabel('Valeurs')
plt.title('Distribution de la grandeur '+ mesure)
plt.axes([0.65, 0.65, 0.2, 0.15])
plt.hist(df_mes, rwidth = 0.8, color = 'royalblue')
plt.title('Histogramme')
#plt.xticks([])
plt.yticks([])

st.pyplot(fig4)

st.markdown(""" **Conclusion**: Tout est en ordre, il n'y a pas de mesure particulière à prendre concernant la distribution des variables numériques.
""")
st.subheader("2.b Variables catégorielles")
# TODO : insérer la rose des vents, avec un choix de station par menu déroulant?