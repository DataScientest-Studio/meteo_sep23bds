import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style = "darkgrid", palette = "colorblind")

from sklearn.metrics import classification_report, confusion_matrix
from joblib import load

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler



rdf = load("../../models/saves/model_saves/save_rdf_SMOTE.joblib")

# Instanciation df 
df = pd.read_csv('../../data/processed/model_weatherAUS.csv')
df.drop(columns = 'Unnamed: 0', inplace = True)
df['Date'] = pd.to_datetime(df['Date'])

# Séparation data / target:
X = df.drop(columns = ['RainTomorrow', 'Date']).copy()
y = df['RainTomorrow'].copy()

# Séparation du jeu d'entrainement et du jeu de test:
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 123, stratify = y) 

# Sauvegarde de test en df:
Xt, yt = X_test, y_test 

# Scale de X_train, X_test:
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Prédictions globales pour afficher la matrice de confusion et le rapport de classification avec le seuil:
preds = rdf.predict_proba(X_test)
y_preds = pd.Series(np.where(preds[:, 1] > 0.66, 1, 0))

################################################################################################

st.title(":gear: Démonstration et conclusion")
st.divider()

st.markdown("Voici les résultats pour notre :orange[meilleur modèle] sur le jeu de test:")


class_rep = pd.DataFrame.from_dict(classification_report(y_test, y_preds, output_dict=True, digits = 2)).T  # création au format df
conf_mat = confusion_matrix(y_test, y_preds)       # Création au format df

st.markdown(""" Rapport de classification:
            """)
st.dataframe(class_rep)

st.markdown(""" Matrice de confusion:
            """)
st.dataframe(conf_mat)

########################################### Bouton Prédiction n°1 #############################################
clic1 = st.button("Faire une prédicition!")
if clic1 == True :
    n = np.random.randint(X_test.shape[0])
    pred = rdf.predict_proba((X_test[n].reshape(1, -1))) # il faut reshape le vecteur à tester. X_test[n].shape = (28, ) et rdf.predict attend un array de dimension 2.
    y_pred = pd.Series(np.where(pred[:, 1] > 0.66, 1, 0))

    if y_pred.array[0] == 1:
        st.write("On prévoit de la pluie :rain_cloud: demain :umbrella_with_rain_drops:.")
    else:
        st.write("On prévoit du beau temps :sun_with_face: demain :sunglasses:  .")
        
    if y_pred.array[0] == y_test.array[n]:  # il faut convertir y_test en array pour pouvoir appeler le nombre correspondant à la ligne n.
        st.write("Cette prédiction est exacte! :heavy_check_mark:")
    else:
        st.write("Cette prédiction est incorrecte... :x:")

############################################ Boutton prédictions n°2 ###########################################
coefficients = rdf.feature_importances_
feats_i = pd.DataFrame({'Feature' : X.columns, 'Importance' : np.abs(coefficients)})
feats_i = feats_i.sort_values('Importance', ascending = False)
new_col = list(feats_i['Feature'])

clic2 = st.button("Essayons de prédire nous-même!")
if clic2 == True :
    n = np.random.choice(Xt.index) # choix d'une ligne par index dans Xt

    ech = Xt.loc[[n]] # double crochets pour avoir un df
    test = scaler.transform(Xt.loc[[n]])
    pred = rdf.predict_proba(test)
    y_pred = pd.Series(np.where(pred[:, 1] > 0.66, 1, 0))

    ech = ech.reindex(columns=new_col)
    st.dataframe(ech)

    if y_pred.array[0] == 1:
        st.write("On prévoit de la pluie :rain_cloud: demain :umbrella_with_rain_drops:.")
    else:
        st.write("On prévoit du beau temps :sun_with_face: demain :sunglasses:  .")

    if y_pred.array[0] == yt[n]:  # il faut convertir y_test en array pour pouvoir appeler le nombre correspondant à la ligne n.
        st.write("Cette prédiction est exacte! :heavy_check_mark:")
    else:
        st.write("Cette prédiction est incorrecte... :x:")
                    