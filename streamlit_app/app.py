from collections import OrderedDict
import streamlit as st
import config
from tabs import introduction, gestionDonnees, dataExploration, modelisation, conclusion


st.set_page_config(
    page_title=config.TITLE,
    page_icon="assets/LFB Logo.svg",
)

with open("style.css", "r") as f:
    style = f.read()

st.markdown(f"<style>{style}</style>", unsafe_allow_html=True)

TABS = OrderedDict(
    [
        (introduction.sidebar_name, introduction),
        (gestionDonnees.sidebar_name, gestionDonnees),
        (dataExploration.sidebar_name, dataExploration),
        (modelisation.sidebar_name, modelisation),
        (conclusion.sidebar_name, conclusion),
    ]
)


def run():
    st.sidebar.image(
        "assets/logo-datascientest.png",
        width = 200,
    )
    tab_name = st.sidebar.radio("", list(TABS.keys()), 0)
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"## {config.PROMOTION}")

    st.sidebar.markdown("### Team members:")
    for member in config.TEAM_MEMBERS:
        st.sidebar.markdown(member.sidebar_markdown(), unsafe_allow_html=True)

    tab = TABS[tab_name]

    tab.run()


if __name__ == "__main__":
    run()
