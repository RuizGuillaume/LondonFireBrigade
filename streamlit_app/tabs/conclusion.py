import streamlit as st
import pandas as pd
import numpy as np


title = "Conclusion"
sidebar_name = "Conclusion"


def run():

    st.title(title)

    st.markdown(
        """
        <div style="text-align: justify;">

        Les performances obtenues par notre modèle peuvent éventuellement sembler relativement faibles comparées aux valeurs que nous avons régulièrement rencontrés dans notre formation, cependant nous faisons face ici à une problématique possédant de nombreux facteurs aléatoires rendant toutes prédictions très difficiles.
        On peut notamment penser à l'activité des pompiers au moment de l’alerte, leurs rapidité pour préparer le matériel, leurs équipements individuels, le trafic routier, la météo, la précision et l'accessibilité de l’adresse de l’incident renseigné par le témoin, etc.

        Finalement, ces résultats, bien que très probablement perfectibles, représentent généralement bien la plupart des délais nécessaires pour que les pompiers arrivent sur les lieux d’incidents signalés sur le numéro d'urgence à Londres.

        Ce type de modèle pourrait permettre à terme à l’opérateur des pompiers de donner au téléphone un temps d’attente approximatif à l'interlocuteur au téléphone.
        De plus, en mettant à jour ce modèle avec de nouvelles données, et en étudiant plus profondément les différents facteurs qui ont un impact sur ces délais, cela pourrait permettre à la ville de Londres d’optimiser ces différents facteurs via des modifications organisationnelles de la London Fire Brigade, voir des modifications d’infrastructure pour fluidifier les interventions.

        Il est aussi important de préciser qu’il serait tout à fait possible d’adapter ce type de modèle à d’autres services publics, dans d’autres villes du monde, à condition que ces derniers effectuent un suivi rigoureux des données liées à leurs activités.
        </div>
        """
        , unsafe_allow_html = True
    )
