import streamlit as st

title = "LONDON FIRE BRIGADE"
sidebar_name = "Introduction"


def run():

    #region Logo
    st.markdown("</br></br>", unsafe_allow_html = True)
    col1, col2, col3 = st.columns(spec = [0.15, 0.7, 0.15])
    with col1:
        st.write('')
    with col2:
        st.image('assets/LFB Logo.svg', use_column_width = True)
    with col3:
        st.write('')
    st.markdown("</br></br>", unsafe_allow_html = True)
    #endregion Logo
    
    st.header("Introduction")
    st.markdown("---")

    st.markdown(
        """
        <div style="text-align: justify;">
        La London Fire Brigade (LFB), fondée en 1833, est le principal service de secours et de lutte contre les incendies au Royaume-Uni. Avec plus de 5000 sapeurs-pompiers professionnels parmi ses 5992 employés, elle est la cinquième plus grande organisation de pompiers au monde, couvrant 1587 kilomètres carrés de Grand Londres et protégeant 8 millions d'habitants.
        Outre ses opérations de lutte contre les incendies, la LFB mène des activités de planification des secours, d'inspection et d'éducation du public.
        </br></br>
        </div>
        """
        , unsafe_allow_html = True
    )
    
    st.subheader("Projet")
    st.markdown("---")
    
    st.markdown(
        """
        <div style="text-align: justify;">
        Cette présentation s'inscrit dans le cadre d'un projet de machine learning dont le code et le rapport sont disponibles sur GitHub. 
        </br></br>
        </div>
        """
        , unsafe_allow_html = True
    )

    st.link_button("Accéder au dépôt GitHub", "https://github.com/DataScientest-Studio/dec23-bds-pompiers")

    st.markdown(
        """
        <div style="text-align: justify;">
        Le but de celui-ci est d'étudier des données gouvernementales publics de la brigade de pompiers de Londres, ainsi que de concevoir un modèle prédictif capable de donner un temps d'intervention approximatif pour que la brigade de pompiers se rendent sur les lieux de l'incident.
        
        Ce temps de réponse correspond à la somme des périodes suivantes :

        - Temps séparant l’instant où l’incident est confirmé par l’opérateur d’appel qui déclenche alors l’ordre de départ et l’instant où l’équipe quitte la caserne avec le camion.

        - Temps séparant l’instant où l’équipe quitte la caserne avec le camion et l’instant où l'équipe arrive sur les lieux de l’incident et commence à traiter celui-ci.

        </div>
        """
        , unsafe_allow_html = True
    )
    
    st.image('assets/Traitement_incident.png',  caption = "Déroulement d'un signalement d'incident")
    
    st.markdown(
        """
        <div style="text-align: justify;">
        Le temps de réponse, représenté par la variable “AttendanceTimeSeconds” correspond donc au temps séparant l'ordre de départ (étape 3) et l'arrivée du camion sur les lieux de l’incident (étape 5).
        </div>
        """
        , unsafe_allow_html = True
        )
