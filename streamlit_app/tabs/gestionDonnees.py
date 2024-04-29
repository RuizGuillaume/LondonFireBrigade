import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import pandas as pd 

title = "Gestion des données"
sidebar_name = "Gestion des données"


def run():

    df = load_data("../Datasets/datasets finaux/dataset_full.csv")

    st.title(title)
    
    st.markdown(
        """
        <div style="text-align: justify;">
        Pour notre projet, nous avons utilisé deux jeux de données distincts :

        - Le premier jeu, provenant du site Web gouvernemental du Royaume-Uni dédié aux données de Londres, détaillant chaque incident depuis janvier 2009, fournissant la date, le lieu et le type de chaque incidents.
        
        - Le second jeu comprend les détails de chaque camion de pompier envoyé sur les lieux d'un incident depuis janvier 2009, incluant l'appareil mobilisé, son lieu de déploiement et les heures de départ et d'arrivée.
        
        Ces deux jeux de données ont été fusionnés en un seul dataset réunissant les descriptions d'incidents et les mobilisations associées, suivant les numéros d'incident (incidentNumber), valeur commune aux deux tables. 
        </div>
        """
        , unsafe_allow_html = True
    )
    
    st.header("Caractéristiques des données")
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: justify;">

        - Le jeu de données final contient 2 270 420 entrées et 59 colonnes, totalisant 1.2Go, avec différents types de données.

        - Certaines colonnes ont un taux élevé de données manquantes, comme "DateAndTimeReturned" avec environ 57,27%.

        - Les valeurs peuvent varier considérablement, par exemple, le temps d'attente varie de 0 à 1200 secondes.

        - Certaines colonnes ont un grand nombre de valeurs uniques, comme "Resource_Code" avec 187 valeurs.

        </div>
        """
        , unsafe_allow_html = True
    )
    
    choices = ["Premières lignes", "Dimensions (lignes, colonnes)", "Description", "Description (inclure les colonnes 'object')"]
    option = st.selectbox("Informations sur le dataset complet", 
                            choices,
                            placeholder = "Choisir le type d'informations souhaitées",
                            index = None,
                            label_visibility = "hidden")

    if option == choices[0]:
        st.dataframe(df.head())
    elif option == choices[1]:
        st.write(df.shape)
    elif option == choices[2]:
        st.dataframe(df.describe())
    elif option == choices[3]:
        st.dataframe(df.describe(include='object'))

    
    st.header("Les variables pertinentes")
    st.markdown("---")
    col = ["IncidentNumber", 
           "CalYear", 
           "HourOfCall", 
           "ResourceMobilisationId", 
           "Resource_Code", 
           "PerformanceReporting", 
            "DateAndTimeMobilised",
            "DateAndTimeMobile",
            "DateAndTimeArrived",
            "TurnoutTimeSeconds",
            "TravelTimeSeconds",
            "AttendanceTimeSeconds",
            "DateAndTimeLeft",
            "DeployedFromStation_Name",
            "DeployedFromLocation",
            "PumpOrder",
            "PlusCode_Code",
            "DateOfCall",
            "IncidentGroup",
            "PropertyCategory",
            "PropertyType",
            "AddressQualifier",
            "Postcode_district",
            "BoroughName",
            "NumCalls"]
    if st.checkbox("Afficher les noms des colonnes conservées"):
        st.dataframe(col)
    
    st.markdown(
        """
        La variable cible est "AttendanceTimeSeconds", et correspond au temps de réponse de la brigade de pompiers.
        """
    )
    
    st.header("Particularités des données")
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: justify;">

        - Les données sont temporelles et détaillées, essentiel pour analyser les performances opérationnelles.

        - La diversité des variables offre de multiples angles d'analyse.

        - Des stratégies spécifiques peuvent être nécessaires pour gérer les données manquantes.

        - Il existe une grande variabilité des valeurs et un nombre élevé de valeurs uniques, reflétant la diversité des situations rencontrées par les services d'incendie.

        </div>
        """
        , unsafe_allow_html = True
    )

    st.header("Preprocessing")
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: justify;">
        De nombreuses modifications ont été apportées pour trier le dataset et conserver les valeurs explicatives de notre variable cible.
        Certaines colonnes ont pu être fusionnées, d'autres ont été supprimées (voir partie modélisation pour constater les colonnes restantes).
        Les valeurs extrêmes de temps de réponse ont aussi été supprimées, certaines casernes ont été écartées car trop peu représentées pour avoir des valeurs statistiquement représentatives, etc.
        </br></br>
        </div>
        """
        , unsafe_allow_html = True
    )

    st.header("Data Engineering")
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: justify;">
        Une information qui instinctivement pourrait avoir un lien avec le temps de réponse serait la distance entre la caserne d'ou part le camion de pompier et le lieux de l'incident.
        La seule chose dont nous ne disposons pas pour calculer la distance est la latitude et la longitude des casernes de pompiers.
        Par chance, l’organisation Open Data Institute (ODI) a déjà travaillé sur une problématique similaire sur les mêmes données de la London Fire Brigade.
        Sur le GitHub de l’ODI est disponible un fichier CSV comportant le nom de la centaine de casernes de pompiers de Londres ainsi que leurs coordonnées GPS.
        En fusionnant le contenu de ce fichier avec notre dataset, puis en convertissant les coordonnées “easting” et “northing” des lieux d’incidents du format OSGB au format WGS84 (format standard de latitude et longitude), on peut appliquer la formule de Haversine pour calculer les distances en mètres entre le lieu d’incident et la caserne d'où part le camion de pompier.
        </div>
        """
        , unsafe_allow_html = True
    )



@st.cache_data
def load_data(filename):
    chunk_size = 50_000 
    chunks = []
    for chunk in pd.read_csv(filename, chunksize = chunk_size):
        chunks.append(chunk)
    
    return pd.concat(chunks, axis = 0)
