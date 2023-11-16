import pandas as pd
import numpy as np
df = pd.read_csv('../data/raw/weatherAUS.csv')
gps =  pd.read_excel('../data/external/station_gps_region.xlsx')

####### Création des colonnes year, month, date ###################
# Mise au format datetime de la colonne 'Date':
df['Date'] = pd.to_datetime(df['Date'])

# Extraction d'informations depuis la variable date
df["Year"] = df['Date'].dt.year # Année:
df["Month"] = df['Date'].dt.month # Mois
df["Day"] = df['Date'].dt.day # Jour du mois

####### Gestion des Rain catégorielles: ############################

# DropNa RainToday et Tomorrow:
df.dropna(subset = ['RainToday', 'RainTomorrow'], inplace = True) # On drop ici pour réaffecter le type de la colonne à entier.

# Numérisation de RainToday et Tomorrow:
df['RainToday'].replace(to_replace = ['Yes', 'No'], value = [1, 0], inplace = True)
df['RainToday'] = df['RainToday'].astype(int)

df['RainTomorrow'].replace(to_replace = ['Yes', 'No'], value = [1, 0], inplace = True)
df['RainTomorrow'] = df['RainTomorrow'].astype(int)

# Encodage des noms des stations:
df['LocationNum'] = df['Location']  # création d'une copie de la colonne 'Location'
df['LocationNum'].replace(to_replace = df['Location'].unique(), value =np.arange(len(df['Location'].unique())), inplace = True ) #remplacement par le code numérique.

############## Numérisation WindGustDir, WindDir9am, WindDir3pm #####

# Création d'un dictionnaire pour convertir, dans « WindGustDir », les directions du vent en radians
WindGustDir_directions_to_radians_dictionary = {
    "N": np.pi / 2,
    "E": 0.0,
    "S": 3 * np.pi,
    "W": np.pi,
    "NE": np.pi / 4,
    "SE": 7 * np.pi / 4,
    "SW": 5 * np.pi / 4,
    "NW": 3 * np.pi / 4,
    "NNE": 0.375 * np.pi,
    "ENE": 0.125 * np.pi,
    "ESE": 1.875 * np.pi,
    "SSE": 1.625 * np.pi,
    "SSW": 1.375 * np.pi,
    "WSW": 1.125 * np.pi,
    "WNW": 0.875 * np.pi,
    "NNW": 0.625 * np.pi
}

# Création des trois colonnes copies numériques:
df['WindGustDirNum'] = df['WindGustDir']
df['WindDir9amNum'] = df['WindDir9am']
df['WindDir3pmNum'] = df['WindDir3pm']

# Remplacement des catégories par les valeurs:
df['WindGustDirNum'].replace(to_replace = WindGustDir_directions_to_radians_dictionary, inplace = True)
df['WindDir9amNum'].replace(to_replace = WindGustDir_directions_to_radians_dictionary, inplace = True)
df['WindDir3pmNum'].replace(to_replace = WindGustDir_directions_to_radians_dictionary, inplace = True)

########## Ajout des données GPS #####################
# Fusion de df et gps pour ajouter les 4 colonnes de gps à df, à savoir: Latitude, Longitude, CodeRegion, NonMes
df = df.merge(right = gps, on = 'Location', how = 'inner')
df.head()

# Encodage des noms des régions:

df['CodeRegionNum'] = df['CodeRegion']  # création d'une copie de la colonne 'Location'
df['CodeRegionNum'].replace(to_replace = df['CodeRegion'].unique(), value =np.arange(len(df['CodeRegion'].unique())), inplace = True ) #remplacement par le code numérique.

# Encodage des noms des valeurs non mesurées:

df['NonMesNum'] = df['NonMes']  # création d'une copie de la colonne 'Location'
df['NonMesNum'].replace(to_replace = df['NonMes'].unique(), value =np.arange(len(df['NonMes'].unique())), inplace = True ) #remplacement par le code numérique.

############### Gestion des nan ##################
# Sélection des variables à remplacer par la moyenne
mean_var = ['MinTemp', 'MaxTemp', 'WindGustSpeed', 'WindSpeed9am', 'WindSpeed3pm', 
            'Humidity9am', 'Humidity3pm', 'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm', 
            'Temp9am', 'Temp3pm', 'Evaporation', 'Sunshine',
            'WindGustDirNum', 'WindDir9amNum', 'WindDir3pmNum']
left_over = ['Rainfall']

#Sélection des variables catégorielles à remplacer par le mode:
mode_var =['WindGustDir', 'WindDir9am', 'WindDir3pm'] # sélection des variables catégorielles à remplacer

# Remplacement des nan par la moyenne ou le mode le plus fréquent:

for station in df['Location'].unique():
    dict_mean_values = {} # Initialisation dictionnaire pour les valeurs moyennes des variables numériques: clé = mesure, valeur = moyenne de la mesure sur tout le tableau
    dict_mode_values = {} # Initialisation dictionnaire pour les valeurs les plus fréquentes des variables catégorielles: clé = mesure, valeur = mode[0] de la mesure sur tout le tableau
    
    # La ligne du dessous permettait de remplacer les nan par la moyenne par station. Elle est inutile maintenant car on remplace brutalement les nan par la moyenne sur le tableau. A garder pour une prochaine update?
    # data = df.loc[df['Location'] == station].copy() # je n'ai pas trouvé d'autre solutions que celle ci, qui me parait un peu lourde niveau mémoire, puisqu'elle nécéssite de créer une copie pour chaque station. Mais je m'arête là car ça marche.
    
    for var in mean_var:   #Création du dictionnaire pour les valeurs moyennes des variables numériques
        if var == 'Cloud9am' or var == 'Cloud3pm':             # Test spécifique sur les Clouds pour arrondir la moyenne
            dict_mean_values[var] = round(df[var].mean(), 0)
        else:
            dict_mean_values[var] = df[var].mean()
    
    for var in mode_var:   #Création du dictionnaire pour les valeurs les plus fréquentes des variables catégorielles
        dict_mode_values[var] = df[var].mode()[0]
    
    df.fillna(value = dict_mean_values, inplace = True)
    df.fillna(value = dict_mode_values, inplace = True)
    #df.fillna(data, inplace = True) inutile ici: servait lors du remplacement des nan par la moyenne de chaque station.
    
## Drop des grandeurs catégorielles:
cat_to_drop = ['Location', 'WindGustDir', 'WindDir9am', 'WindDir3pm', 'CodeRegion', 'NonMes']
df.drop(columns = cat_to_drop, inplace = True)

# Création du csv final prêt pour la modélisation
df.to_csv('../data/processed/model_weatherAUS.csv')