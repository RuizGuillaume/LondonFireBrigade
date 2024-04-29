import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


title = "Exploration des données"
sidebar_name = "Exploration des données"


def run():

    #region Chargement des données
    df = load_data("../Datasets/datasets finaux/dataset.csv")
    df_full = load_data("../Datasets/datasets finaux/dataset_full.csv")

    df['DateOfCall'] = pd.to_datetime(df['DateOfCall'])
    df_full['DateAndTimeMobilised'] = pd.to_datetime(df_full['DateAndTimeMobilised'])
    #endregion
    
    #region Introduction
    st.title(title)

    st.markdown(
        """
        <div style="text-align: justify;">
        Pour commencer, notons qu'à ce stade nos données ont été traitées, certaines valeurs de temps de réponse, distances, et type d'incidents ont été exclus du dataset car peu représentatifs des phénomènes que l'on souhaite étudier.
        Si vous souhaitez obtenir plus de précisions et visualisations des données brutes, nous vous invitons à consulter le rapport en cliquant sur le bouton ci-dessous.
        </br></br>
        </div>
        """
        , unsafe_allow_html = True
    )

    st.link_button("Voir le rapport de projet", "https://github.com/DataScientest-Studio/dec23-bds-pompiers/blob/main/London%20Fire%20Brigade%20-%20Report.pdf")

    st.header("Visualisation")
    st.markdown("---")

    st.markdown(
        """
        <div style="text-align: justify;">
        Pour mieux comprendre les données, certaines notions importantes ayant un impact sur nos modèles peuvent être observées ici à l'aide de graphique.
        Les informations relatives aux types d'incidents et aux évolutions des temps de réponse des brigades de pompiers sont représentées graphiquement ci-dessous.
        </br></br>
        </div>
        """
        , unsafe_allow_html = True
    )
    #endregion

    #region Type d'incidents
    st.subheader("Type d'incidents")

    st.markdown(
    """
    <div style="text-align: justify;">
    Les incidents déclarés à la LFB peuvent être de différentes natures : incendie, accident de la route, incident médical, etc.
    Les graphiques suivants présentent la fréquence de signalement de ces différents types d'incidents, et l'impact de cette information sur le temps de réponse des pompiers.
    </div>
    """
    , unsafe_allow_html = True
    )

    choices = ["Nombre d'occurence par type d'incident", "Temps de réponse moyen par type d'incident"]
    option = st.selectbox("Type de graphique concernant les incidents", 
                            choices,
                            placeholder = "Selectionnez un type de graphique",
                            index = None,
                            label_visibility = "hidden")


    if option == choices[0]:

        grpIncidents = df.IncidentType.value_counts()

        fig2 = go.Figure(go.Bar(
                    x = list(grpIncidents),
                    y = list(grpIncidents.index),
                    orientation = 'h',
                    ))

        fig2.update_layout(height = 600, width = 1600, title = "Types d'incidents",
                        xaxis = dict(title = "Nombre d'incidents"),
                        yaxis = dict(title = "Type d'incident", categoryorder = "total descending"))

        st.plotly_chart(fig2, use_container_width = True)
        st.markdown('<p style="font-size:12px; ">RTC = Road Traffic Collision  |  AFA = Automatic Fire Alarm</p>', unsafe_allow_html=True)

    elif option == choices[1]:

        grpIncidents = df.AttendanceTimeSeconds.groupby([df['IncidentType']]).mean()

        fig3 = go.Figure(go.Bar(
                    x = list(grpIncidents),
                    y = list(grpIncidents.index),
                    orientation = 'h'
                    ))
        fig3.update_layout(height = 600, width = 1600, title = "Types d'incidents",
                        xaxis = dict(title = "Temps de réponse moyen (en secondes)"),
                        yaxis = dict(title = "Type d'incident", categoryorder = "total descending"))
        
        st.plotly_chart(fig3, use_container_width = True)
        st.markdown('<p style="font-size:12px; ">RTC = Road Traffic Collision  |  AFA = Automatic Fire Alarm</p>', unsafe_allow_html=True)

    #endregion
        
    #region Temps de réponse
    st.subheader("Temps de réponse")
    
    st.markdown(
    """
    <div style="text-align: justify;">
    Pour concevoir un modèle de machine learning capable de prédire des temps de réponse des brigades de pompiers, il est intéressant de pouvoir visualiser soit même quelles sont les variables ayant un impact sur celui-ci.  
    Les graphiques suivants présentent la distribution de notre variable cible, son évolution au cours du temps ainsi que son évolution en fonction de la distance séparant la caserne de pompiers d'où part le camion et le lieu de l'incident.
    </div>
    """
    , unsafe_allow_html = True
    )

    choices = ["Distribution du temps de réponse", "Evolution du temps de réponse annuel", "Evolution du temps de réponse au sein d'une journée", "Evolution du temps de réponse en fonction de la distance"]
    option = st.selectbox("Type de graphique concernant les temps de réponse", 
                            choices,
                            placeholder = "Selectionnez un type de graphique",
                            index = None,
                            label_visibility = "hidden")

    
    if option == choices[0]:

        ResponseTime = df.AttendanceTimeSeconds

        fig = make_subplots(rows = 2, cols = 1, shared_xaxes = True, vertical_spacing = 0, row_heights = [600, 250])
        fig.append_trace(go.Histogram(x = ResponseTime, showlegend=False), row = 1, col = 1)
        fig.append_trace(go.Box(x = ResponseTime, fillcolor = "#a4adf8", line = dict(color = "#636efa"), showlegend = False, marker = dict(opacity = 0.01)), row = 2, col = 1)
        fig.update_layout(width = 1800, title_text="Distribution du temps de réponse en secondes des pompiers de Londres", yaxis2 = dict(visible = False))
        fig.update_xaxes(range = [93, 676])

        st.plotly_chart(fig, use_container_width = True)

    elif option == choices[1]:

        ResponseTimeByYear = df_full.AttendanceTimeSeconds.groupby([df_full['DateAndTimeMobilised'].dt.year]).mean()

        fig4 = px.bar(x = ResponseTimeByYear.index , y = ResponseTimeByYear, title = "Évolution du temps de réponse moyen en secondes par an", width = 1600, color = ResponseTimeByYear, color_continuous_scale='Blues', range_color=(150, ResponseTimeByYear.max()))
        fig4.update_layout(
            xaxis = dict(title = "Année"),
            yaxis = dict(title = "Temps de réponse moyen (en secondes)")
        )

        st.plotly_chart(fig4, use_container_width = True)

    elif option == choices[2]:

        ResponseTimeByHour = df.AttendanceTimeSeconds.groupby([df['DateOfCall'].dt.hour]).mean()

        fig5 = px.bar(y = ResponseTimeByHour, title = "Évolution du temps de réponse moyen en secondes au sein d'une journée", color = ResponseTimeByHour, color_continuous_scale='Blues', range_color=(150, ResponseTimeByHour.max()))
        fig5.update_layout(
            width = 1600,
            xaxis = dict(
                title = "Heure de la journée",
                tickmode = "array",
                tickvals = list(range(24)),
                ticktext = ['00h', '01h', '02h', '03h', '04h', '05h', '06h', '07h', '08h', '09h', '10h', '11h', '12h', '13h', '14h', '15h', '16h', '17h', '18h', '19h', '20h', '21h', '22h', '23h']
            ),
            yaxis = dict(title = "Temps de réponse moyen (en secondes)")   
        )

        st.plotly_chart(fig5, use_container_width = True)

    elif option == choices[3]:

        dfChart = df
        intervalle = 500 # Intervalle en mètres à determiner
        dfChart['intervalle_distance'] = pd.cut(dfChart['Distance'], bins = range(0, dfChart['Distance'].max() + intervalle, intervalle), right = False)
        temps_moyen_par_intervalle = dfChart.groupby('intervalle_distance', observed=False)['AttendanceTimeSeconds'].mean().reset_index()
        temps_moyen_par_intervalle['intervalle_distance'] = temps_moyen_par_intervalle['intervalle_distance'].astype(str)

        # Création du bar chart
        fig6 = px.bar(
            x = temps_moyen_par_intervalle['intervalle_distance'],
            y = temps_moyen_par_intervalle['AttendanceTimeSeconds'],
            width = 1600,
            color = temps_moyen_par_intervalle['AttendanceTimeSeconds'],
            color_continuous_scale='Blues',
            range_color = (0, temps_moyen_par_intervalle['AttendanceTimeSeconds'].max())
        )

        # Mise en forme du graphique
        fig6.update_layout(
            title = "Temps de réponse moyen par intervalle de distance",
            xaxis_title = "Intervalle de distance (mètres)",
            yaxis_title = "Temps de réponse moyen (secondes)"
        )

        # Affichage du graphique
        st.plotly_chart(fig6, use_container_width = True)
        st.markdown(
        """
        <div style="text-align: justify;">
        Comme indiqué dans la partie 'Feature Engineering' de la page précédente, ces intervalles de temps ont été calculés via les coordonnées OSGB des lieux d'incidents et les coordonnées WGS84 des casernes de pompiers à l'aide de la formule de Haversine (plus d'informations dans le rapport et le notebook d'exploration des données).
        On constate effectivement une croissance du temps de trajet, et donc du temps de réponse total, des brigades de pompiers en fonction de la distance les séparant du lieu d'intervention. 
        </div>
        """
        , unsafe_allow_html = True
        )
    #endregion

@st.cache_data
def load_data(filename):
    chunk_size = 50_000 
    chunks = []
    for chunk in pd.read_csv(filename, chunksize = chunk_size):
        chunks.append(chunk)
    
    return pd.concat(chunks, axis = 0)
