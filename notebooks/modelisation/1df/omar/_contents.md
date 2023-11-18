modélisations par omar

système de nomenclature
exemple : `3.1.2-oc-clf-time-E-S-C9-C3-KNN-DTW.ipynb`
- `3.1.2` : numéro de notebook
  - `3` : dataset
    - `1` : `ready_Evaporation.csv`
    - `2` : `ready_Evaporation_Sunshine.csv`
    - `3` : `ready_Evaporation_Sunshine_Cloud9am_Cloud3pm.csv`
    - `4` : `ready_all.csv`
    - `5` : `ready_Cloud9am_Cloud3pm.csv`
    - `6` : `ready_Evaporation_Sunshine_WindGustDir_WindGustSpeed_Pressure9am_Pressure3pm_WindGustDirNum.csv`
    - `7` : `ready_Evaporation_Sunshine_Pressure9am_Pressure3pm_Cloud9am_Cloud3pm.csv`
    - `8` : `ready_Sunshine.csv`
    - `9` : `ready_WindGustDir_WindGustSpeed_WindGustDirNum.csv`
    - `10` : `model_weatherAUS.csv`
  - `1` : algorithme
    - `1` : KNN + DTW
    - `2` : TSF
    - `3` : ROCKET
  - `2` : variation
    - `0` : TTS
    - `1` : TSS
    - `2` : sort + TSS
    - `3` : sort + TSS + StandardScaler
    - `4` : sort + TSS + tslearn
    - `5` : sort + TSS + SMOTE
    - `6` : sort + TSS + StandardScaler + RandomUnderSampler
    - `7` : sort + TSS + StandardScaler + RandomUnderSampler + tslearn
    - `8` : sort + TSS + MinMaxScaler
    - `9` : sort + TSS + MinMaxScaler + tslearn
- `oc` : auteur
- `clf-time` : approche
- `E-S-C9-C3` : dataset
- `KNN-DTW` : algorithme