import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Prévision météo en Australie", page_icon=":partly_sunny:"
)


# = SIDEBAR =
with st.sidebar:
    st.header(":partly_sunny: Prévision météo en Australie")
    st.markdown(
        "Un projet de _data science_ réalisé par [Alexandre WINGER](https://github.com/alexandrewinger) et [Omar CHOA](https://www.linkedin.com/in/omarchoa/)."
    )


tab_1, tab_2, tab_3, tab_4, tab_5 = st.tabs(
    [
        ":telescope: **Changer d'angle**",
        ":spider_web: **KNN-DTW**",
        ":deciduous_tree: **TSF**",
        ":rocket: **ROCKET**",
        ":gear: **_Preprocessing_ +**",
    ]
)


with tab_1:
    # = PAGE =
    st.title(":mantelpiece_clock: Séries temporelles")

    ## == SECTION ==
    st.header(":telescope: Changer d'angle")

    st.write("\n")

    ### === SOUS-SECTION ===
    st.subheader("Notre jeu de données")

    st.markdown("- Observations pour **plusieurs variables** dans le **temps**")
    st.markdown("- Une **série temporelle multivariée**")

    st.write("\n")

    ### === SOUS-SECTION ===
    st.subheader("Boîte à outils")

    st.markdown("- `scikit-learn` : **données tabulaires** (variables i.i.d)")
    st.markdown("- `sktime` : `scikit-learn` pour **séries temporelles**")

    st.write("\n")

    ### === SOUS-SECTION ===
    st.subheader("Algorithmes de classification retenus")

    st.markdown("- Approches **distances :** KNN-DTW")
    st.markdown("- Approches **intervalles :** TSF")
    st.markdown("- Approches **dictionnaires :** ROCKET")


with tab_2:
    # = PAGE =
    st.title(":mantelpiece_clock: Séries temporelles")

    ## == SECTION ==
    st.header(":spider_web: KNN-DTW")

    st.write("\n")

    ### === SOUS-SECTION ===
    st.subheader("Présentation")

    st.markdown(
        "- _K Nearest Neighbors_ (KNN) avec _Dynamic Time Warping_ (DTW) comme **métrique de distance**"
    )
    st.markdown(
        "- DTW :  mesure la **similarité** entre séries temporelles avec **vitesses différentes**"
    )
    st.markdown("- 1NN-DTW : _benchmark_ / _gold standard_ ")

    st.write("\n")

    st.image("../../reports/figures/series_temp_knn_dtw.png")
    st.caption(
        "Source : Regan, 2023. [« K Nearest Neighbors & Dynamic Time Warping »](https://github.com/markdregan/K-Nearest-Neighbors-with-Dynamic-Time-Warping)."
    )

    st.write("\n")

    ### === SOUS-SECTION ===
    st.subheader("Implémentation")

    st.code(
        """from sktime.classification.distance_based import KNeighborsTimeSeriesClassifier

clf = KNeighborsTimeSeriesClassifier(n_neighbors=1, distance="dtw")

clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)"""
    )


with tab_3:
    # = PAGE =
    st.title(":mantelpiece_clock: Séries temporelles")

    ## == SECTION ==
    st.header(":deciduous_tree: TSF")

    st.write("\n")

    ### === SOUS-SECTION ===
    st.subheader("Présentation")

    st.markdown("- _Time Series Forest_ (TSF)")
    st.markdown("- Adaptation de _Random Forest_ (RF) aux séries temporelles")
    st.markdown(
        "- **Entraînement** d'un arbre de décision par **intervalle temporel distinct,** puis **vote d'ensemble**"
    )

    st.write("\n")

    st.image("../../reports/figures/series_temp_tsf.png", width=450)
    st.caption(
        "Source : Deng et al., 2013. [« A time series forest for classification and feature extraction »](https://doi.org/10.1016/j.ins.2013.02.030)."
    )

    st.write("\n")

    ### === SOUS-SECTION ===
    st.subheader("Implémentation")

    st.code(
        """from sktime.classification.interval_based import TimeSeriesForestClassifier

clf = TimeSeriesForestClassifier(n_estimators=200, min_interval=3)

clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)"""
    )


with tab_4:
    # = PAGE =
    st.title(":mantelpiece_clock: Séries temporelles")

    ## == SECTION ==
    st.header(":rocket: ROCKET")

    st.write("\n")

    ### === SOUS-SECTION ===
    st.subheader("Présentation")

    st.markdown("- _RandOm Convolutional KErnel Transform_")
    st.markdown("- S'inspire des **réseaux de neurones convolutifs**")
    st.markdown(
        "- **Transformation** des séries temporelles à l'aide de noyaux de convolution aléatoires, puis **entraînement** d’un classificateur linéaire"
    )

    st.write("\n")

    st.image("../../reports/figures/series_temp_rocket.png")
    st.caption(
        "Source : aeon. [« Convolution-based time series classification in aeon »](https://www.aeon-toolkit.org/en/latest/examples/classification/examples/classification/convolution_based.html)."
    )

    st.write("\n")

    ### === SOUS-SECTION ===
    st.subheader("Implémentation")

    st.code(
        """from sktime.transformations.panel.rocket import Rocket
from sklearn.linear_model import SGDClassifier

trf = Rocket(num_kernels=10000)
clf = SGDClassifier(loss="log_loss")

X_train = trf.fit_transform(X_train)
X_test = trf.transform(X_test)

clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)"""
    )


with tab_5:
    # = PAGE =
    st.title(":mantelpiece_clock: Séries temporelles")

    ## == SECTION ==
    st.header(":gear: _Preprocessing_ +")

    st.write("\n")

    ### === SOUS-SECTION ===
    st.subheader("Tri")

    st.markdown("- **Condition :** données doivent être classées par `Date`")
    st.markdown("- **Problème :** elles sont classées par `Location`")
    st.markdown("- **Solution :** indexation par `Date`, puis tri par index")

    st.write("\n")

    ### === SOUS-SECTION ===
    st.subheader("Découpage")

    st.markdown(
        "- **Condition :** `X_train` et `y_train` doivent être plus anciens que `X_test` et `y_test`"
    )
    st.markdown(
        "- **Problème :** `train_test_split` (basé sur `ShuffleSplit`) applique un découpage aléatoire"
    )
    st.markdown("- **Solution :**  `TimeSeriesSplit` (basé sur `KFold`)")

    st.write("\n")

    col_1, col_2 = st.columns(2)
    with col_1:
        st.image("../../reports/figures/split_shuffle.png")
    with col_2:
        st.image("../../reports/figures/split_time_series.png")
    st.caption(
        "Source : scikit-learn. [« Visualizing cross-validation behavior in scikit-learn »](https://scikit-learn.org/stable/auto_examples/model_selection/plot_cv_indices.html)."
    )

    st.write("\n")

    ### === SOUS-SECTION ===
    st.subheader("Conversion")

    st.markdown("- **Condition :** données doivent être dans un format compatible")
    st.markdown("- **Problème :** DataFrames `pandas` standard non compatibles")

    st.markdown("- **Solution** pour KNN-DTW : conversion en `numpy3D`")
    with st.expander("Exemple"):
        st.code(
            """
array([[[ 1,  2,  3],
        [ 4,  5,  6]],

       [[ 1,  2,  3],
        [ 4, 55,  6]],

       [[ 1,  2,  3],
        [42,  5,  6]]])
            """
        )

    st.markdown(
        "- **Solution** pour TSF : conversion en `numpy3D`, puis application de `ColumnConcatenator` (de `sktime`)"
    )
    with st.expander("Exemple"):
        st.code(
            """
array([[[ 1,  2,  3,  4,  5,  6]],

       [[ 1,  2,  3,  4, 55,  6]],

       [[ 1,  2,  3, 42,  5,  6]]])
            """
        )

    st.markdown(
        "- **Solution** pour ROCKET : conversion en `Panel` par application de `to_sktime_dataset` (de `tslearn`)"
    )
    with st.expander("Exemple"):
        X_train_Panel_head = pd.read_csv(
            "../../data/processed/omar/X_train_Panel_head.csv", index_col=0
        )
        st.dataframe(X_train_Panel_head)

    st.write("\n")

    st.image("../../reports/figures/series_temp_crane.png")
    st.caption(
        "Source : Izbicki, 2011. [« Converting images into time series for data mining »](https://izbicki.me/blog/converting-images-into-time-series-for-data-mining.html)."
    )
