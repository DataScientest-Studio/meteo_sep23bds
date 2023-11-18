import pandas as pd


def numpyfy(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    X_to_numpy: bool = True,
):
    """

    Cette fonction convertit en arrays les 4 jeux de données issus du
    découpage effectué par le splitter (train_test_split / TimeSeriesSplit)
    afin de les rendre compatibles avec `sktime`.

    Arguments :

        X_train (DataFrame) : données explicatives du jeu d'entraînement
        X_test (DataFrame) : données explicatives du jeu de test
        y_train (Series) : données cibles du jeu d'entraînement
        y_test (Series) : données cibles du jeu de test
        X_to_numpy (Boolean) :
            - précise si X_train et X_test doivent être convertis en arrays
            avant d'être remodelés
            - valeur par défaut : `True` (X_train et X_test sont des
            DataFrames)
            - si X_train et X_test sont déjà des arrays (notamment après
            transformation par un scaler, indiquer `False`)

    Retourne :

        X_train_np (array de 3 dimensions) : données explicatives du jeu
        d'entraînement, remodelées selon la structure suivante :

            - Dimension 1 (num_instances) : nombre d'INSTANCES de séries
            temporelles. Pour cette étude, dont l'unité temporelle est le
            jour, nous considérons 1 jour comme 1 instance.

            - Dimension 2 (num_variables) : nombre de VARIABLES EXPLICATIVES
            par instance de série temporelle.

            - Dimension 3 (length) : nombre de POINTS TEMPORELS observés par
            instance de série temporelle. Pour cette étude, comme l'unité
            temporelle est le jour, chaque instance de série temporelle
            correspond à 1 seul point temporel.

            (Référence :
            https://www.sktime.net/en/latest/examples/02_classification.html)

        X_test_np (array de 3 dimensions) : données explicatives du jeu de
        test, remodelées selon la structure ci-dessus.

        y_train_np (array de 1 dimension) : données cibles du jeu
        d'entraînement.

        y_test_np (array de 1 dimension) : données cibles du jeu de test.

    """

    # Récupération des dimensions

    X_train_d1, X_train_d2 = X_train.shape
    X_test_d1, X_test_d2 = X_test.shape

    # Conversion des DataFrames `X` en arrays de 3 dimensions

    if X_to_numpy is True:
        X_train_np = X_train.to_numpy().reshape(X_train_d1, X_train_d2, 1)
        X_test_np = X_test.to_numpy().reshape(X_test_d1, X_test_d2, 1)
    elif X_to_numpy is False:
        X_train_np = X_train.reshape(X_train_d1, X_train_d2, 1)
        X_test_np = X_test.reshape(X_test_d1, X_test_d2, 1)

    # Conversion des Series `y` en arrays de 1 dimension

    y_train_np = y_train.to_numpy()
    y_test_np = y_test.to_numpy()

    # Sortie des arrays convertis

    return X_train_np, X_test_np, y_train_np, y_test_np
