import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
import joblib


title = "Modélisation"
sidebar_name = "Modélisation"


def run():
    
    #region Préparation des données
    # Importation du dataset et selection des colonnes
    df_og = load_data("../Datasets/datasets finaux/dataset.csv")
    df_lr = df_og.drop(["IncidentNumber", "IncidentType", "DateOfCall"], axis = 1)
    df = df_og.drop(["IncidentNumber", "DateOfCall"], axis = 1)

    # Standardisation des données numériques
    global scaler
    scaler = StandardScaler()
    df[["Distance", "AttendanceTimeSeconds"]] = scaler.fit_transform(df[["Distance", "AttendanceTimeSeconds"]])
    global scaler_lr
    scaler_lr = StandardScaler()
    df_lr[["Distance", "AttendanceTimeSeconds"]] = scaler_lr.fit_transform(df_lr[["Distance", "AttendanceTimeSeconds"]])

    # Encodage One-hot
    df = pd.get_dummies(df, dtype="int")
    df_lr = pd.get_dummies(df_lr, dtype="int")

    # Séparation des variables explicatives et de la variable cible
    X = df.drop("AttendanceTimeSeconds", axis = 1)
    y = df.AttendanceTimeSeconds
    X_lr = df_lr.drop("AttendanceTimeSeconds", axis = 1)
    y_lr = df_lr.AttendanceTimeSeconds

    # Division du dataset en datasets d'entrainement et de validation, les 20% d'enregistrements les plus récents serviront de dataset de validation
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
    global X_train, X_test, y_train, y_test
    X_train = X[:-round(0.2*len(X))]
    X_test = X[-round(0.2*len(X)):]
    y_train = y[:-round(0.2*len(y))]
    y_test = y[-round(0.2*len(y)):]
    global X_train_lr, X_test_lr, y_train_lr, y_test_lr
    X_train_lr = X_lr[:-round(0.2*len(X_lr))]
    X_test_lr = X_lr[-round(0.2*len(X_lr)):]
    y_train_lr = y_lr[:-round(0.2*len(y_lr))]
    y_test_lr = y_lr[-round(0.2*len(y_lr)):]
    #endregion

    #region Modèles
    lr_model = joblib.load('../models/LBF_LinearRegression')
    en_model = joblib.load('../models/LBF_ElasticNet')
    sgdr_model = joblib.load('../models/LBF_SGDRegressor')
    dt_model = joblib.load('../models/LBF_DecisionTreeModel')
    gbr_model = joblib.load('../models/LBF_GradientBoostingRegressor')
    #endregion

    #region Texte
    st.title(title)
    st.subheader("Préparation des données")
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: justify;">

        - Les données comprennent les colonnes "BoroughName", "IncidentType", "Station_Name", "Distance", et la variable cible "AttendanceTimeSeconds".

        - Le jeu de données contient 2 156 331 lignes sans valeurs manquantes.

        - Les variables numériques ont été standardisées avec StandardScaler pour harmoniser leurs distributions.

        - Les variables catégorielles ont été encodées en one-hot pour une utilisation dans des modèles de régression.

        </div>
        """
        , unsafe_allow_html = True
    )

    st.subheader("Identification du problème")
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: justify;">

        - L'objectif est de prédire le temps de réponse des pompiers en fonction des informations fournies lors de l'appel d'urgence.

        - Cela implique une tâche de régression, visant à anticiper une mesure quantitative.
        </div>
        """
        , unsafe_allow_html = True
    )
    
    st.subheader("Choix des métriques")
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: justify;">

        - Le modèle sera évalué en minimisant le MSE et en maximisant le coefficient de détermination R².

        - Les métriques sélectionnées incluent MSE, RMSE et R² pour évaluer la précision et la qualité des modèles.
        </div>
        """
        , unsafe_allow_html = True
    )
    
    st.subheader("Choix du modèle et optimisation")
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: justify;">

        - Plusieurs algorithmes de régression ont été explorés, avec DecisionTreeRegressor retenu comme le plus performant.

        - DecisionTreeRegressor a démontré une capacité à capturer les relations non-linéaires entre les variables.

        - L'arbre de décision a obtenu un R² de 0.51 avec un MSE légérement inférieur aux autres modèles grâce à une optimisation des hyperparamètres.

        - L'importance des variables a été confirmée par l'analyse de l'arbre de décision.
        </div>
        """
        , unsafe_allow_html = True
    )
    #endregion

    #region Modèles et métriques
    choices = ["Régression linéaire", "Elastic Net", "Descente de gradient stochastique", "Arbre de décision", "Gradient Boosting pour la régression"]
    option = st.selectbox("Modèles", 
                            choices,
                            placeholder = "Selectionnez un type de modèle",
                            index = 0,
                            label_visibility = "hidden")
    global model
    is_linearRegression = False
    if option == choices[0]:
        model = lr_model
        is_linearRegression = True
    if option == choices[1]:
        model = en_model
        is_linearRegression = False
    if option == choices[2]:
        model = sgdr_model
        is_linearRegression = False
    if option == choices[3]:
        model = dt_model
        is_linearRegression = False
    if option == choices[4]:
        model = gbr_model
        is_linearRegression = False


    if model is None:
        st.write('Veuillez choisir un modèle.')
    else:
        st.write('Le modèle choisi est :', option)

        metric = st.radio('Que souhaitez-vous montrer ?', ('R²', 'MSE', 'RMSE'))
        metric_train, metric_test = get_metric(model, metric, is_linearRegression)
        col1, col2 = st.columns(2)
        with col1:
            st.write('Score', metric, "en entrainement :", metric_train)  
        with col2:
            st.write('Score', metric, "en validation :", metric_test)  

    #endregion

    #region Prédiction
    st.subheader("Prédiction")
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: justify;">

        L'interface ci-dessous permet de saisir des informations pour effectuer des prédictions de temps de réponse à l'aide de notre modèle d'arbre de décision.
        N'hésitez pas à faire varier les différents paramètres pour se rendre compte de l'évolution du résultat. Vous constaterez que la distance a un impact très important sur la prédiction.

        </div>
        """
        , unsafe_allow_html = True
    )
    
    col1, col2 = st.columns(2)
    with col1:
        choices = sorted(df_og["IncidentType"].unique())
        option_IncidentType = st.selectbox("Type d'incident", 
                                choices,
                                placeholder = "Selectionnez un type d'incident",
                                index = 0)
        
        input_Distance = st.number_input("Distance en mètres", min_value = 0, max_value = 7000, value = 1250)

    with col2:
        choices = sorted(df_og["BoroughName"].unique())
        option_BoroughName = st.selectbox("Nom d'arrondissement", 
                                choices,
                                placeholder = "Selectionnez un arrondissement",
                                index = 0)
        
        choices = sorted(df_og["Station_Name"].unique())
        option_Station_Name = st.selectbox("Nom de la caserne", 
                                choices,
                                placeholder = "Selectionnez une caserne de pompier",
                                index = 0)
    

    # Création du dataframe de test
    df_prediction = pd.DataFrame(columns = df.columns)
    df_prediction.loc[0] = [0] * len(df_prediction.columns)

    # Récupération des informations saisies pour la prédiction
    cols = ["BoroughName_" + option_BoroughName, "IncidentType_" + option_IncidentType, "Station_Name_" + option_Station_Name, "Distance"]
    df_prediction[cols] = (1, 1, 1, input_Distance)

    # Préprocessing
    df_prediction[["Distance", "AttendanceTimeSeconds"]] = scaler.transform(df_prediction[["Distance", "AttendanceTimeSeconds"]])
    df_prediction = df_prediction.drop("AttendanceTimeSeconds", axis = 1)

    # Prédiction
    prediction = pd.DataFrame(columns = ["Distance", "AttendanceTimeSeconds"])
    prediction.loc[0] = (df_prediction.iloc[0]["Distance"], dt_model.predict(df_prediction)[0])

    # Affichage de la prédiciton
    prediction_inverse = scaler.inverse_transform(prediction)
    st.write("Notre modèle prédit un temps de réponse de", round(prediction_inverse[0, 1]), "secondes.")
    #endregion

#region Fonctions
def get_metric(modele, choice, is_linearRegression):
    '''
    Fonction pour calculer les scores en fonction du modèle et de la métrique choisie
    '''
    
    if is_linearRegression:

        X_train_metric = X_train_lr
        X_test_metric = X_test_lr
        y_train_metric = y_train_lr
        y_test_metric = y_test_lr

        scaler_metric = scaler_lr
    else:
        X_train_metric = X_train
        X_test_metric = X_test
        y_train_metric = y_train
        y_test_metric = y_test

        scaler_metric = scaler

    y_pred_train = modele.predict(X_train_metric)
    y_pred_test = modele.predict(X_test_metric)

    if choice == 'R²':
        return (round(r2_score(y_train_metric, y_pred_train), 2), round(r2_score(y_test_metric, y_pred_test), 2))
    else:

        # Inversion du scale pour les métriques MSE et RMSE à l'échelle.
        y_train_metric_for_unscaled = pd.DataFrame(columns = ["Distance", "AttendanceTimeSeconds"])
        y_train_metric_for_unscaled["Distance"] = X_train_metric["Distance"] 
        y_train_metric_for_unscaled["AttendanceTimeSeconds"] = y_train_metric
        y_test_metric_for_unscaled = pd.DataFrame(columns = ["Distance", "AttendanceTimeSeconds"])
        y_test_metric_for_unscaled["Distance"] = X_test_metric["Distance"]
        y_test_metric_for_unscaled["AttendanceTimeSeconds"] = y_test_metric
        y_pred_train_for_unscaled = pd.DataFrame(columns = ["Distance", "AttendanceTimeSeconds"])
        y_pred_train_for_unscaled["Distance"] = X_train_metric["Distance"] 
        y_pred_train_for_unscaled["AttendanceTimeSeconds"] = y_pred_train
        y_pred_test_for_unscaled = pd.DataFrame(columns = ["Distance", "AttendanceTimeSeconds"])
        y_pred_test_for_unscaled["Distance"] = X_test_metric["Distance"] 
        y_pred_test_for_unscaled["AttendanceTimeSeconds"] = y_pred_test

        y_train_metric = scaler_metric.inverse_transform(y_train_metric_for_unscaled)[:,1]
        y_test_metric = scaler_metric.inverse_transform(y_test_metric_for_unscaled)[:,1]
        y_pred_train = scaler_metric.inverse_transform(y_pred_train_for_unscaled)[:,1]
        y_pred_test = scaler_metric.inverse_transform(y_pred_test_for_unscaled)[:,1]

        if choice == 'MSE':
            return (round(mean_squared_error(y_train_metric, y_pred_train), 2), round(mean_squared_error(y_test_metric, y_pred_test), 2))
        elif choice == 'RMSE':
            return (round(np.sqrt(mean_squared_error(y_train_metric, y_pred_train)), 2), round(np.sqrt(mean_squared_error(y_test_metric, y_pred_test)), 2))


@st.cache_data
def load_data(filename):
    chunk_size = 50_000 
    chunks = []
    for chunk in pd.read_csv(filename, chunksize = chunk_size):
        chunks.append(chunk)
    
    return pd.concat(chunks, axis = 0)
#endregion