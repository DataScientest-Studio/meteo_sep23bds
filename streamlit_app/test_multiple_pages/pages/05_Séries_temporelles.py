import streamlit as st


tab_1, tab_2, tab_3, tab_4, tab_5 = st.tabs(
    [
        ":telescope: Changer d'angle",
        ":spider_web: KNN-DTW",
        ":deciduous_tree: TSF",
        ":rocket: ROCKET",
        ":gear: _Preprocessing_ +",
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
        "- _K-Nearest Neighbors_ (KNN) avec _Dynamic Time Warping_ (DTW) comme **métrique de distance**"
    )
    st.markdown(
        "- DTW :  mesure la **similarité** entre séries temporelles avec **vitesses différentes**"
    )
    st.markdown("- 1NN-DTW : _benchmark_ / _gold standard_ ")

    st.write("\n")

    st.image(
        "../../reports/figures/series_temp_knn_dtw.png",
        caption="Source : M. Regan, « K Nearest Neighbors & Dynamic Time Warping ». 5 décembre 2023. Disponible sur : https://github.com/markdregan/K-Nearest-Neighbors-with-Dynamic-Time-Warping",
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

    st.image(
        "../../reports/figures/series_temp_tsf.png",
        caption="Source : H. Deng, G. Runger, E. Tuv, et M. Vladimir, « A time series forest for classification and feature extraction », Information Sciences, vol. 239, p. 142-153, août 2013, doi: 10.1016/j.ins.2013.02.030.",
        width=480,
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

    st.image(
        "../../reports/figures/series_temp_rocket.png",
        caption="Source : « Convolution based time series classification in aeon », aeon. Disponible sur : https://www.aeon-toolkit.org/en/latest/examples/classification/examples/classification/convolution_based.html",
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

    st.markdown("_Suite_")
